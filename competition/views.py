from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from datetime import timedelta
from django.utils.timezone import now
from django.shortcuts import get_object_or_404


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from djangorestframework_camel_case.parser import CamelCaseFormParser
from rest_framework.parsers import MultiPartParser, FormParser


from .models import Competition
from users.models import CustomUser
from matchtype.models import MatchType
from applicant_info.models import ApplicantInfo
from applicant.models import Applicant
from .serializers import CompetitionListSerializer, CompetitionDetailInfoSerializer, CompetitionApplyInfoSerializer, CompetitionApplySerializer
from applicant_info.serializers import ApplicantInfoSerializer, CompetitionApplicantInfoSerializer
from applicant.serializers import ApplicantSerializer, CompetitionApplicantSerializer
from users.serializers import UserWithClubInfoSerializer




## 대회 리스트
class CompetitionListView(APIView):
    """
    대회 리스트
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        # 쿼리 파라미터로부터 gender와 type 가져옴
        gender = request.query_params.get('gender')
        type = request.query_params.get('match_type')

        if gender and type:
            competitions = Competition.objects.filter(match_type__gender=gender, match_type__type=type)
        else:
            competitions = Competition.objects.all()

        serializer = CompetitionListSerializer(competitions, many=True, context={'request': request})
        
        return Response(serializer.data)
    

## 대회 상세정보
class CompetitionDetailView(APIView):
    """
    대회 상세보기
    """
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            competition = Competition.objects.get(pk=pk)
            serializer = CompetitionDetailInfoSerializer(competition, context={'request': request})
            return Response(serializer.data)
        except Competition.DoesNotExist:
            return Response({'error': '대회를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)



# 파트너 조회
class PartnerSearchView(APIView):
    """
    파트너 검색
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='파트너 검색',
        operation_description='쿼리파라미터를 사용하여 파트너 검색 결과 목록을 불러온다 (예시 /api/v1/competitions/1/partnersearch/?query=검색어)',
        manual_parameters=[
            openapi.Parameter('query', openapi.IN_QUERY, description="ex) 유", type=openapi.TYPE_STRING),
        ],
        responses={
            200: UserWithClubInfoSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )

    def get(self, request, pk):
        search_query = request.query_params.get('query', '')
        
        if not search_query:
            return Response({'error': '검색어를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 검색어에 따라 사용자 필터링
        partners = CustomUser.objects.filter(username__icontains=search_query)
        serializer = UserWithClubInfoSerializer(partners, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


## 대회신청
class CompetitionApplyView(APIView):
    """
    대회 신청
    """

    permission_classes = [IsAuthenticated]
    parser_classes = (CamelCaseFormParser, MultiPartParser)
    
    def post(self, request, pk):
        
        try: # 대회 조회
            competition = Competition.objects.get(pk=pk)
        except Competition.DoesNotExist:
            return Response({'error': '대회를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # 코드 확인
        submitted_code = request.data.get('code')
        if submitted_code != competition.code:
            return Response({'error': '제출된 코드가 유효하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        applicant = request.user # 신청자 = 로그인한 유저
        print(request.user)


        # 신청자 중복 신청 확인
        if Applicant.objects.filter(applicant_info__competition=competition, user=applicant).exists():
            return Response({'error': '이미 신청된 대회입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 진행 중인 대회 신청시 에러메세지
        if competition.status == 'during':
            return Response({'error': '진행중인 대회에는 신청할 수 없습니다.'})
        
        # 끝낸 대회 신청시 에러메세지
        if competition.status == 'ended':
            return Response({'error': '종료된 대회입니다.'})


        # 신청자 성별이 대회에 적합한지 확인
        if competition.match_type.gender != ('mix','team'): # 대회가 혼성이나 팀 경기가 아니고
            if competition.match_type.gender != applicant.gender:
                return Response({'error': f'이 대회는 {competition.match_type.gender} 경기이므로 신청할 수 없습니다.'})
                        
        # 티어 구분         
        if competition.tier != applicant.tiers:
            print(competition.tier)
            print(applicant.tiers)
            #return Response({'error': '실력 제한 규정으로 참가 신청을 할 수 없습니다.'})
            return Response({'error': f'대회 티어:{competition.tier.id} 신청자 티어:{applicant.tiers.id}'})




        ### 단식 신청
        if competition.match_type.type == 'single':
            return self.handle_singles(request, competition, applicant)
        
        
        
        ### 복식 신청
        if competition.match_type.type == 'double':
            # 파트너 생성
            partner_id = request.data.get('partner_id')  #신청 폼에서 제공된 파트너의 ID
            
            # 파트너 선택 확인
            if not partner_id:
                    return Response({'error': '파트너를 선택하세요.'}, status=status.HTTP_400_BAD_REQUEST)
            
            partner = CustomUser.objects.get(id=partner_id) # 파트너 인스턴스 생성
            
            # 혼성 확인
            if competition.match_type.gender == 'mix' and applicant.gender == partner.gender:
                return Response({'error': '혼성 경기는 서로 다른 성별의 파트너가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 파트너 성별 확인
            elif partner.gender != competition.match_type.gender and competition.match_type.gender != 'mix':
                return Response({'error': '선택한 파트너의 성별이 경기의 조건과 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
            # 자기 자신 선택 불가
            elif applicant.id == partner.id:
                return Response({'error': '본인을 파트너로 선택할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 파트너 티어 확인
            elif partner.tiers.id != competition.tier.id:
                return Response({'error': '선택한 파트너 부가 경기의 조건과 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            # 파트너 중복 신청 확인
            elif partner_id and Applicant.objects.filter(applicant_info__competition=competition, user_id=partner_id).exists():
                return Response({'error': '선택하신 파트너는 이미 해당 대회를 신청하셨습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            return self.handle_doubles(request, competition, applicant, partner)
        
        else:
            return Response({'error': '대회신청이 정상적으로 진행되지 않았습니다. 신청정보를 확인해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
    
    ### 단식 신청 처리 로직
    def handle_singles(self, request, competition, applicant):
        
        # 대기 처리
        current_applicants_count = ApplicantInfo.objects.filter(competition=competition).count()
        max_participants = competition.max_participants
        waiting_number = None
        
        # 대기자 처리 
        if current_applicants_count >= max_participants:
            max_waiting_number = ApplicantInfo.objects.filter(competition=competition, waiting_number__isnull=False).count()
            waiting_number = max_waiting_number + 1
        
        # applicant_info 저장       
        applicant_info_data = {
                    'competition': competition.id,
                    'waiting_number': waiting_number,
                    'expired_date': now() + timedelta(days=competition.deposit_date)
            }
        serializer = ApplicantInfoSerializer(data=applicant_info_data)
        if serializer.is_valid():
            applicant_info = serializer.save() 
        else:
                return Response(ApplicantInfoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        # applicant 저장
        expired_date = applicant_info_data['expired_date']
        applicant_data = {'user': applicant.id, 'applicant_info': applicant_info.id}
        applicant_serializer = ApplicantSerializer(data=applicant_data)
        if applicant_serializer.is_valid():
            applicant_serializer.save()  # 신청자 생성
            
            # 대회신청 / 대기신청 응답
            applicant_info_status = '대기신청 완료' if waiting_number else '신청 완료'
            competition_serializer = CompetitionApplySerializer(competition)
            response_data = {
                'status': f'{applicant_info_status}',
                'applicant_info': {
                    'applicant': applicant.username,
                    'phone': applicant.phone
                },
                'competition_info': competition_serializer.data,
                'expired_date': expired_date  
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(applicant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    ### 복식 신청 처리 로직
    def handle_doubles(self, request, competition, applicant, partner):
        with transaction.atomic(): # 2개 신청 동시 처리
            
            current_applicants_count = ApplicantInfo.objects.filter(competition=competition).count()
            max_participants = competition.max_participants
            waiting_number = None
            
            # 대기자 처리
            if current_applicants_count >= max_participants:
                max_waiting_number = ApplicantInfo.objects.filter(competition=competition, waiting_number__isnull=False).count()
                waiting_number = max_waiting_number + 1
            
            # applicant_info 저장 
            applicant_info_data = {
                    'competition': competition.id,
                    'waiting_number': waiting_number,
                    'expired_date': now() + timedelta(days=competition.deposit_date)
            }
            serializer = ApplicantInfoSerializer(data=applicant_info_data)
            if serializer.is_valid():
                applicant_info = serializer.save()
            else:
                return Response(ApplicantInfoSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            expired_date = applicant_info_data['expired_date']
            saved_applicants = []
            
            for user in [applicant, partner]:
                applicant_data = {'user': user.id, 'applicant_info': applicant_info.id}
                applicant_serializer = ApplicantSerializer(data=applicant_data)
                if not applicant_serializer.is_valid():
                    return Response(applicant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                saved_applicant = applicant_serializer.save() # 신청자 생성
                saved_applicants.append(saved_applicant) # 신청자 리스트 생성(복식 경우 2명의 신청자 return)
            
            # 대회신청 / 대기신청 응답    
            applicant_info_status = '대기신청 완료' if waiting_number else '신청 완료'
            competition_serializer = CompetitionApplySerializer(competition)
            response_data = {
                'status': f'{applicant_info_status}',
                'applicant_info': {
                    'applicant': applicant.username,
                    'phone': applicant.phone
                },
                'competition_info': competition_serializer.data,
                'expired_date': expired_date  
            }

        return Response(response_data, status=status.HTTP_201_CREATED)
    

class CompetitionApplyResultView(APIView):
    """
    대회 신청 결과 조회
    """

    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        
        user = request.user
        
        # 대회를 찾을 수 없는 경우
        try :
            competition = Competition.objects.get(pk=pk)
        except Competition.DoesNotExist :
            return Response({'error':'존재하지 않는 대회입니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # 단식 대회의 경우
        if competition.match_type.type == 'single':
        
            try :
                applicant_1 = Applicant.objects.get(applicant_info__competition=competition)
            except Applicant.DoesNotExist :
                return Response({'error':'신청자 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

            applicant1_serializer = CompetitionApplicantSerializer(applicant_1)
            
            applicants = applicant1_serializer.data

            
                
        # 복식 대회의 경우
        else : 
            try :
                applicant_1, applicant_2 = Applicant.objects.filter(applicant_info__competition=competition)
            except Applicant.DoesNotExist :
                return Response({'error':'신청자 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
            applicant1_serializer = CompetitionApplicantSerializer(applicant_1)
            applicant2_serializer = CompetitionApplicantSerializer(applicant_2)

            applicants = [applicant1_serializer.data, applicant2_serializer.data]


        # 대회 신청정보
        applicant_infos = applicant_1.applicant_info

        applicant_info_serializer = CompetitionApplicantInfoSerializer(applicant_infos)
        competition_serializer = CompetitionApplySerializer(competition)
        return Response(['applicant_list :', applicants, 
                        'applicant_info :', applicant_info_serializer.data, 
                        'competition :', competition_serializer.data], 
                        status=status.HTTP_200_OK)



class CompetitionCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        # 신청 정보 변수 생성
        applicant_info = get_object_or_404(ApplicantInfo, pk=pk)

        # 현재 로그인한 사용자가 해당 ApplicantInfo에 속한 Applicant 중 하나인지 확인
        if not Applicant.objects.filter(applicant_info=applicant_info, user=request.user).exists():
            return Response({'error': '이 작업을 수행할 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        # 사용자가 취소할 수 있는 상태인지 확인
        if applicant_info.status in ['사용자 취소', '관리자 취소']:
            return Response({'error': '이미 취소 처리된 신청입니다.'}, status=status.HTTP_409_CONFLICT)
        
        # 신청 상태를 '사용자 취소'로 업데이트
        applicant_info.status = '사용자 취소'
        applicant_info.save()
        
        waiting_applicant = ApplicantInfo.objects.all().order_by('waiting_number').first()
        print(waiting_applicant)
        if waiting_applicant:
            # 대기자를 참가자로 변경
            if waiting_applicant.status == '입금 대기':
                waiting_applicant.waiting_number = None
            elif waiting_applicant.status == '참가 대기중':
                waiting_applicant.waiting_number = None
                waiting_applicant.status = '참가 완료'

        # 업데이트된 정보를 반환
        serializer = ApplicantInfoSerializer(applicant_info)
        return Response(serializer.data, status=status.HTTP_200_OK)
