from django.utils import timezone
from django.db.models import Sum, Window, F
from django.db.models.functions import Rank
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Point
from rest_framework.response import Response
from .serializers import RealtimeUserRankingSerializer, RealtimeTeamRankingSerializer




# 실시간 유저 랭킹 조회 API
class RealtimeUserRankingView(APIView):
    @swagger_auto_schema(
        operation_summary='실시간 유저 랭킹 조회',
        operation_description='쿼리파라미터를 사용하여 매치타입별(팀x) 데이터를 불러올 수 있음 (예시 /api/v1/ranking/realtime/user?gender=male&type=single)',
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
                raise NotFound(detail="No rankings found for the given match type.")
            
            # 순위를 계산하여 각 객체에 할당
            for idx, obj in enumerate(queryset, start=1):
                obj.rank = idx

            serializer = RealtimeUserRankingSerializer(queryset, many=True)
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
        operation_description='쿼리파라미터를 사용하여 매치타입별(팀o) 데이터를 불러올 수 있음 (예시 /api/v1/ranking/realtime/team?gender=team&type=team)',
        manual_parameters=[
            openapi.Parameter('gender', openapi.IN_QUERY, description="ex) team", type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY, description="ex) team", type=openapi.TYPE_STRING)
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
                raise NotFound(detail="해당 매치 타입에 대한 랭킹이 없습니다.")
            
            # 순위를 계산하여 각 객체에 할당
            for idx, obj in enumerate(queryset, start=1):
                obj.rank = idx

            serializer = RealtimeTeamRankingSerializer(queryset, many=True)
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
            for idx, obj in enumerate(queryset, start=1):
                obj.rank = idx
                
        
                
            # 로그인 상태에 따라 my_ranking 정보를 다르게 설정
            my_ranking = None
            if request.user.is_authenticated:
                user_rank = None
                for idx, obj in enumerate(queryset, start=1):
                    if obj.user == request.user:
                        user_rank = obj
                        user_rank.rank = idx  # 사용자의 순위를 객체에 직접 할당
                        break
                
                if user_rank:
                    # RealtimeUserRankingSerializer를 이용하여 사용자의 랭킹 정보 시리얼라이즈 진행
                    serializer = RealtimeUserRankingSerializer(user_rank)
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
        manual_parameters=[
            openapi.Parameter('gender', openapi.IN_QUERY, description="ex) team", type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY, description="ex) team", type=openapi.TYPE_STRING)
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
            # 쿼리 파라미터
            match_type_param = request.query_params.get('type')
            gender_param = request.query_params.get('gender')
            
            if match_type_param:
                queryset = queryset.filter(match_type__type=match_type_param)
            if gender_param:
                queryset = queryset.filter(match_type__gender=gender_param)

            # 각 팀의 총 포인트 합산 및 내림차순 정렬 / annotate : 쿼리셋에 집계 값을 추가할 때 사용)
            queryset = queryset.annotate(total_points=Sum('points')).order_by('-total_points')
            
            if not queryset.exists():
                raise NotFound(detail="해당 매치 타입에 대한 랭킹이 없습니다.")
            
            # 순위를 계산하여 각 객체에 할당
            for idx, obj in enumerate(queryset, start=1):
                obj.rank = idx

            # 로그인 상태에 따라 my_team_ranking 정보를 다르게 설정
            my_team_ranking = None
            if request.user.is_authenticated:
                team_rank = None
                for idx, obj in enumerate(queryset, start=1):
                    if obj.team == request.user.team:
                        team_rank = obj
                        team_rank.rank = idx  # 사용자의 순위를 객체에 직접 할당
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