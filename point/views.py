from django.utils import timezone
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.views import APIView
from .models import Point
from rest_framework.response import Response
from .serializers import RealtimeUserRankingSerializer, RealtimeTeamRankingSerializer




# 실시간 유저 랭킹 조회 API
class RealtimeUserRankingView(APIView):
    @swagger_auto_schema(
        operation_summary='실시간 유저 랭킹 조회',
        operation_description='쿼리파라미터를 사용하여 매치타입별 데이터 및 유저명 조회 가능 (예시 /api/v1/ranking/realtime/user?gender=male&type=single&name=오태식)',
        manual_parameters=[
            openapi.Parameter('gender', openapi.IN_QUERY, description="ex) male", type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY, description="ex) single", type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="ex) 김", type=openapi.TYPE_STRING)
        ],
        responses={
            200: RealtimeUserRankingSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            current_time = timezone.now()
            # 기본 필터: timezone now 기준 만료되지 않은 승점을 수집
            queryset = Point.objects.filter(expired_date__gte=current_time)
            
            # 기본적인 매치 타입과 젠더에 대한 필터링
            match_type_param = request.query_params.get('type')
            gender_param = request.query_params.get('gender')
            if match_type_param:
                queryset = queryset.filter(match_type__type=match_type_param)
            if gender_param:
                queryset = queryset.filter(match_type__gender=gender_param)
            
            # 타입과 젠더에 따라 필터링된 쿼리셋에 대해 포인트 합산 진행
            queryset = queryset.annotate(total_points=Sum('points')).order_by('-total_points')
            # 필터링된 쿼리셋에 대하여 순위 계산
            ranked_queryset = []
            for idx, obj in enumerate(queryset, start=1):
                obj.rank = idx
                ranked_queryset.append(obj)
            
            # 이름으로 필터링 진행
            name_param = request.query_params.get('name')
            if name_param:
                ranked_queryset = [obj for obj in ranked_queryset if name_param.lower() in obj.user.username.lower()]
            
            if not ranked_queryset:
                raise NotFound(detail='조건에 맞는 랭킹이 없습니다.')
            
            serializer = RealtimeUserRankingSerializer(ranked_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        except NotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
        

# 실시간 팀 랭킹 조회 API
class RealtimeTeamRankingView(APIView):
    @swagger_auto_schema(
        operation_summary='실시간 팀 랭킹 조회',
        operation_description='실시간 팀 랭킹을 조회 및 쿼리파라미터를 활용하여 팀명 조회 가능 (예시 /api/v1/ranking/realtime/team?name=라온테니스)',
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="ex) 김", type=openapi.TYPE_STRING)
        ],
        responses={
            200: RealtimeTeamRankingSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            current_time = timezone.now()
            # 기본 필터: timezone now 기준 만료되지 않은 승점을 수집
            queryset = Point.objects.filter(expired_date__gte=current_time)
            
            # match_type이 'team'인 경우만 필터링
            queryset = queryset.filter(match_type__type='team')
            
            # 각 팀의 총 포인트 합산 및 내림차순 정렬
            queryset = queryset.annotate(total_points=Sum('points')).order_by('-total_points')
            
            if not queryset.exists():
                raise NotFound(detail='해당 매치 타입에 대한 랭킹이 없습니다.')
            
            # 순위를 계산하여 각 객체에 할당
            ranked_queryset = []
            for idx, obj in enumerate(queryset, start=1):
                obj.rank = idx
                ranked_queryset.append(obj)
            
            # 쿼리 파라미터에서 'team_name'을 받아옴
            team_name_param = request.query_params.get('name')
            
            # 'team_name' 파라미터가 존재하면 해당 이름을 포함하는 팀으로 필터링
            if team_name_param:
                ranked_queryset = [obj for obj in ranked_queryset if team_name_param.lower() in obj.team.name.lower()]
            
            if not ranked_queryset:
                raise NotFound(detail='해당 팀 이름에 대한 랭킹이 없습니다.')
            
            serializer = RealtimeTeamRankingSerializer(ranked_queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except NotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
        
        
        
        
 # 실시간 나의 랭킹 조회 API     
class RealtimeMyRankingView(APIView):
    @swagger_auto_schema(
        operation_summary='실시간 나의 랭킹 조회',
        operation_description='로그인한 사용자의 랭킹 정보를 조회합니다.',
        manual_parameters=[
            openapi.Parameter('gender', openapi.IN_QUERY, description="ex) male", type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY, description="ex) single", type=openapi.TYPE_STRING)
        ],
        responses={
            200: RealtimeUserRankingSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            current_time = timezone.now()
            # 기본 필터: timezone now 기준 만료되지 않은 승점을 수집
            queryset = Point.objects.filter(expired_date__gte=current_time)
            # 쿼리 파라미터
            match_type_param = request.query_params.get('type')
            gender_param = request.query_params.get('gender')
            
            if match_type_param:
                queryset = queryset.filter(match_type__type=match_type_param)
            if gender_param:
                queryset = queryset.filter(match_type__gender=gender_param)

            # 각 유저의 총 포인트 합산 및 내림차순 정렬 / annotate : 쿼리셋에 집계 값을 추가할 때 사용)
            queryset = queryset.annotate(total_points=Sum('points')).order_by('-total_points')

            if not queryset.exists():
                raise NotFound(detail='해당 매치타입에 대한 랭킹을 찾을 수 없습니다.')
            
            # 순위를 계산하여 각 객체에 할당
            ranked_queryset = []
            for idx, obj in enumerate(queryset, start=1):
                obj.rank = idx
                ranked_queryset.append(obj)
                
        
                
            # 로그인 상태에 따라 my_ranking 정보를 다르게 설정
            my_ranking = None
            user_rankings = []
            if request.user.is_authenticated:
                for obj in ranked_queryset:
                    if obj.user == request.user:
                        user_rankings.append(obj)
                
                if user_rankings:
                    # RealtimeUserRankingSerializer를 이용하여 사용자의 랭킹 정보 시리얼라이즈 진행
                    serializer = RealtimeUserRankingSerializer(user_rankings, many=True)
                    my_ranking = serializer.data
                else:
                    my_ranking = '참가한 대회가 없습니다.'
            else:
                my_ranking = '로그인이 필요합니다.'

            return Response(my_ranking, status=status.HTTP_200_OK)

        except NotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        
    
    
    
# 실시간 나의 팀 랭킹 조회 API
class RealtimeMyTeamRankingView(APIView):
    @swagger_auto_schema(
        operation_summary='실시간 나의 팀 랭킹 조회',
        operation_description='로그인한 유저가 속한 팀의 랭킹 정보를 조회합니다.',
        responses={
            200: RealtimeTeamRankingSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            current_time = timezone.now()
            # 기본 필터: timezone now 기준 만료되지 않은 승점을 수집
            queryset = Point.objects.filter(expired_date__gte=current_time)
            
            # match_type이 'team'인 경우만 필터링
            queryset = queryset.filter(match_type__type='team')

            # 각 유저의 총 포인트 합산 및 내림차순 정렬 / annotate : 쿼리셋에 집계 값을 추가할 때 사용)
            queryset = queryset.annotate(total_points=Sum('points')).order_by('-total_points')
            
            if not queryset.exists():
                raise NotFound(detail='해당 매치 타입에 대한 랭킹이 없습니다.')
            
            # 순위를 계산하여 각 객체에 할당
            ranked_queryset = []
            for idx, obj in enumerate(queryset, start=1):
                obj.rank = idx
                ranked_queryset.append(obj)

            # 로그인 상태에 따라 my_team_ranking 정보를 다르게 설정
            my_team_ranking = None
            if request.user.is_authenticated:
                team_rank = None
                for obj in ranked_queryset:
                    if obj.team == request.user.team:
                        team_rank = obj # obj가 request.user와 같은 팀에 속할 때 실행.
                        break
                
                if team_rank:
                    # RealtimeTeamRankingSerializer를 이용하여 유저가 속한 팀 랭킹 정보 시리얼라이즈 진행
                    serializer = RealtimeTeamRankingSerializer(team_rank)
                    my_team_ranking = serializer.data
                else:
                    my_team_ranking = '참가한 대회가 없습니다.'
            else:
                my_team_ranking = '로그인이 필요합니다.'

            return Response(my_team_ranking, status=status.HTTP_200_OK)

        except NotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)