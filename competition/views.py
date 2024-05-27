from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from datetime import timedelta
from django.utils.timezone import now

from .models import Competition
from users.models import CustomUser
from matchtype.models import MatchType
from applicant_info.models import ApplicantInfo
from applicant.models import Applicant
from .serializers import CompetitionListSerializer, CompetitionDetailInfoSerializer, CompetitionApplyInfoSerializer, CompetitionApplySerializer
from applicant_info.serializers import ApplicantInfoSerializer
from applicant.serializers import ApplicantSerializer

 
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


## 대회신청
class CompetitionApplyView(APIView):
    """
    대회 신청
    """
    permission_classes = [IsAuthenticated]
    
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
        # 신청자 중복 신청 확인
        if Applicant.objects.filter(applicant_info__competition=competition, user=applicant).exists():
            return Response({'error': '해당 대회에 이미 신청하셨습니다.'}, status=status.HTTP_400_BAD_REQUEST)
                        
        
        
        ### 단식 신청
        if competition.match_type.type == 'single':
            return self.handle_singles(request, competition, applicant)
        
        
        
        ### 복식 신청
        if competition.match_type.type == 'double':
            # 파트너 생성
            partner_id = request.data.get('partner_id')  #신청 폼에서 제공된 파트너의 ID
            
            # 파트너 선택 확인
            if not partner_id:
                    return Response({'error': '파트너가 입력되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            partner = CustomUser.objects.get(id=partner_id) # 파트너 인스턴스 생성
            
            # 혼성 확인
            if competition.match_type.gender == 'mix' and applicant.gender == partner.gender:
                return Response({'error': '혼성 경기는 서로 다른 성별의 파트너가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
            # 파트너 성별 확인
            elif partner.gender != competition.match_type.gender and competition.match_type.gender != 'mix':
                return Response({'error': '파트너 성별이 해당 대회에는 신청 불가능합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
            # 자기 자신 선택 불가
            elif applicant.id == partner.id:
                return Response({'error': '신청자 본인을 파트너로 선택할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 파트너 티어 확인
            elif partner.tier != competition.tier:
                return Response({'error': '파트너 부가 달라 신청 불가능합니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            # 파트너 중복 신청 확인
            elif partner_id and Applicant.objects.filter(applicant_info__competition=competition, user_id=partner_id).exists():
                return Response({'error': '선택하신 파트너는 이미 해당 대회를 신청하셨습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            return self.handle_doubles(request, competition, applicant, partner)
        
        else:
            return Response({'error': '대회신청이 정상적으로 되지 않았습니다. 신청정보를 확인해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
    
    ### 단식 신청 처리 로직
    def handle_singles(self, request, competition, applicant):
        
        # 대기 처리
        current_applicants_count = ApplicantInfo.objects.filter(competition=competition).count()
        max_participants = competition.max_participants
        waiting_number = None
        
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
            applicant_serializer.save()
            
            # 대기/정상 신청 응답
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
            
            #대기 처리
            current_applicants_count = ApplicantInfo.objects.filter(competition=competition).count()
            max_participants = competition.max_participants
            waiting_number = None
            
            if current_applicants_count >= max_participants:
                max_waiting_number = ApplicantInfo.objects.filter(competition=competition, waiting_number__isnull=False).count()
                waiting_number = max_waiting_number + 1
            
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
                saved_applicant = applicant_serializer.save()
                saved_applicants.append(saved_applicant)
                
            applicant_info_status = '대기신청 완료' if waiting_number else '신청 완료'
            competition_serializer = CompetitionApplySerializer(competition)
            response_data = {
                'status': f'{applicant_info_status}',
                'applicant_info': {
                    'first_appicant': {
                        'appliant': saved_applicants[0].user.username,
                        'phone': saved_applicants[0].user.phone
                        },
                    'second_appicant': {
                        'appliant': saved_applicants[1].user.username,
                        'phone': saved_applicants[1].user.phone
                        }
                    },
                'competition_info': competition_serializer.data,
                'expired_date': expired_date                    
                }

        return Response(response_data, status=status.HTTP_201_CREATED)