from django.utils import timezone
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.views import APIView
from .models import Point
from rest_framework.response import Response
from .serializers import UserRankingSerializer, TeamRankingSerializer
import datetime
from django.contrib.auth import get_user_model
from team.models import Team
from tier.models import Tier

User = get_user_model()


# 유저 랭킹 조회 API
class UserRankingView(APIView):
    @swagger_auto_schema(
        operation_summary='실시간/연도별 유저 랭킹 조회',
        operation_description='쿼리파라미터를 사용하여 연도별 / 매치타입별 / 티어별 / 유저이름별 필터 조회 가능(예시 /api/v1/ranking/user?year=2023&gender=male&type=single&tier=OO부&name=오태식)',
        manual_parameters=[
            openapi.Parameter('year', openapi.IN_QUERY, description="default= 실시간 랭킹", type=openapi.TYPE_INTEGER),
            openapi.Parameter('gender', openapi.IN_QUERY, description="default= male", type=openapi.TYPE_STRING),
            openapi.Parameter('type', openapi.IN_QUERY, description="default= single", type=openapi.TYPE_STRING),
            openapi.Parameter('tier', openapi.IN_QUERY, description="default= All", type=openapi.TYPE_INTEGER),
            openapi.Parameter('name', openapi.IN_QUERY, description="default= All", type=openapi.TYPE_STRING)
        ],
        responses={
            200: UserRankingSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def get(self, request, *args, **kwargs):
        year_param = request.query_params.get('year')
        
        if year_param:
            year = int(year_param)
            end_of_year = datetime.datetime(year, 12, 31, 23, 59, 59)
            queryset = Point.objects.filter(
                created_at__lt=end_of_year,
                expired_date__gte=end_of_year
            )
        else:
            current_time = timezone.now()
            queryset = Point.objects.filter(expired_date__gte=current_time)
        
        match_type_param = request.query_params.get('type', 'single')
        gender_param = request.query_params.get('gender', 'male')
        tier_param = request.query_params.get('tier')
        
        if match_type_param:
            queryset = queryset.filter(match_type__type=match_type_param)
        if gender_param:
            queryset = queryset.filter(match_type__gender=gender_param)
        if tier_param:
            try:
                tier_param = int(tier_param)
                queryset = queryset.filter(tier__id=tier_param)
            except ValueError:
                raise NotFound(detail='유효하지 않은 티어 값입니다.')
        
        queryset = queryset.values('user', 'tier').annotate(total_points=Sum('points')).order_by('-total_points')
        
        ranked_queryset = []
        for idx, obj in enumerate(queryset, start=1):
            user_id = obj['user']
            user = User.objects.get(id=user_id)
            tier_id = obj['tier']
            tier = Tier.objects.get(id=tier_id)
            obj['user'] = user 
            obj['tier'] = tier
            obj['rank'] = idx
            ranked_queryset.append(obj)
        
        name_param = request.query_params.get('name')
        if name_param:
            ranked_queryset = [obj for obj in ranked_queryset if name_param.lower() in obj['user'].username.lower()]
        
        if not ranked_queryset:
            return Response({'detail': '조건에 맞는 랭킹이 없습니다.'}, status=status.HTTP_200_OK)
        
        serializer = UserRankingSerializer(ranked_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        
        
        
        
        
        

# 팀 랭킹 조회 API
class TeamRankingView(APIView):
    @swagger_auto_schema(
        operation_summary='실시간/연도별 팀 랭킹 조회',
        operation_description='쿼리파라미터를 사용하여 연도별 / 팀 이름별 필터 조회 가능 (예시 /api/v1/ranking/team?name=라온테니스)',
        manual_parameters=[
            openapi.Parameter('year', openapi.IN_QUERY, description="ex) default = 실시간", type=openapi.TYPE_INTEGER),
            openapi.Parameter('name', openapi.IN_QUERY, description="ex) default = All", type=openapi.TYPE_STRING)
        ],
        responses={
            200: TeamRankingSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            # 쿼리 파라미터에서 연도 값을 가져옴
            year_param = request.query_params.get('year')
            
            if year_param:
                year = int(year_param)
                # 해당 연도의 끝
                end_of_year = datetime.datetime(year, 12, 31, 23, 59, 59)
                
                # 해당 연도 이전에 생성된 승점이고, 해당 연도 말까지 만료되지 않은 승점 필터링
                queryset = Point.objects.filter(
                    created_at__lt=end_of_year, # lt = 작다
                    expired_date__gte=end_of_year # gte= 크거나 같다
                )
            else:
                # 기본 필터: 현재 시간 기준 만료되지 않은 승점을 필터링 (쿼리파라미터에 빈 값 일때)
                current_time = timezone.now()           
                queryset = Point.objects.filter(expired_date__gte=current_time)
            
            # match_type이 'team'인 경우만 필터링
            queryset = queryset.filter(match_type__type='team')
            
            # 각 팀의 총 포인트 합산 및 내림차순 정렬
            queryset = queryset.values('team').annotate(total_points=Sum('points')).order_by('-total_points')
            
            if not queryset.exists():
                return Response({'detail': '조건에 맞는 랭킹이 없습니다.'}, status=status.HTTP_200_OK)
            
            # 순위를 계산하여 각 객체에 할당
            ranked_queryset = []
            for idx, obj in enumerate(queryset, start=1):
                team_id = obj['team']
                team = Team.objects.get(id=team_id)
                obj['team'] = team
                obj['rank'] = idx
                ranked_queryset.append(obj)
                
            
            # 쿼리 파라미터에서 'team_name'을 받아옴
            team_name_param = request.query_params.get('name')
            
            # 'team_name' 파라미터가 존재하면 해당 이름을 포함하는 팀으로 필터링
            if team_name_param:
                ranked_queryset = [obj for obj in ranked_queryset if team_name_param.lower() in obj['team'].name.lower()]
            
            if not ranked_queryset:
                raise NotFound(detail='해당 팀 이름에 대한 랭킹이 없습니다.')
            
            serializer = TeamRankingSerializer(ranked_queryset, many=True)
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
            openapi.Parameter('type', openapi.IN_QUERY, description="ex) single", type=openapi.TYPE_STRING),
        ],
        responses={
            200: UserRankingSerializer(many=True),
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
            
            # 로그인된 사용자의 티어 정보를 가져옴           
            if request.user.is_authenticated:
                user_tiers = request.user.tiers.all()
                
                # 사용자가 속한 모든 매치 타입을 가져옴
                if not match_type_param or not gender_param:
                    queryset = queryset.filter(
                        match_type__in=[tier.match_type for tier in user_tiers]
                    )
                else:
                    user_tier_ids = [tier.id for tier in user_tiers]
                    queryset = queryset.filter(tier__in=user_tier_ids)
                    # # 사용자의 티어와 매치 타입(젠더, 타입)이 일치하는지 확인
                    # match_type_filtered_tiers = []
                    # for tier in user_tiers:
                    #     if tier.match_type.type == match_type_param and tier.match_type.gender == gender_param:
                    #         match_type_filtered_tiers.append(tier)

                    # # 매치타입과 일치하는 티어가 있을 경우, 해당 티어의 매치 타입에 따라 queryset을 필터링
                    # if match_type_filtered_tiers:
                    #     queryset = queryset.filter(
                    #         match_type__in=[tier.match_type for tier in match_type_filtered_tiers]
                    #     )
                    # # 사용자가 속한 티어와 매치되는 티어가 없을 경우, 비어 있는 쿼리셋을 반환
                    # else:
                    #     queryset = queryset.none()


            # 각 유저의 총 포인트 합산 및 내림차순 정렬 / annotate : 쿼리셋에 집계 값을 추가할 때 사용)
            queryset = queryset.values('user', 'tier').annotate(total_points=Sum('points')).order_by('-total_points')

            if not queryset:
                return Response({"detail": "참가한 대회가 없습니다."}, status=200)
            
            # 순위를 계산하여 각 객체에 할당
            ranked_queryset = []
            for idx, obj in enumerate(queryset, start=1):
                user_id = obj['user']
                user = User.objects.get(id=user_id)
                tier_id = obj['tier']
                tier = Tier.objects.get(id=tier_id)
                obj['user'] = user
                obj['tier'] = tier
                obj['rank'] = idx
                ranked_queryset.append(obj)
                
        
                
            # 로그인 상태에 따라 my_ranking 정보를 다르게 설정
            if request.user.is_authenticated:
                user_rankings = [obj for obj in ranked_queryset if obj['user'] == request.user]
                if user_rankings:
                    # UserRankingSerializer를 이용하여 사용자의 랭킹 정보 시리얼라이즈 진행
                    serializer = UserRankingSerializer(user_rankings, many=True)
                    my_ranking = serializer.data
                else:
                    return Response({"detail": "참가한 대회가 없습니다."}, status=status.HTTP_200_OK)
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
            200: TeamRankingSerializer(many=True),
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
            queryset = queryset.values('team').annotate(total_points=Sum('points')).order_by('-total_points')
            
            if not queryset:
                return Response({"detail": "참가한 대회가 없습니다."}, status=200)
            
            # 순위를 계산하여 각 객체에 할당
            ranked_queryset = []
            for idx, obj in enumerate(queryset, start=1):
                team_id = obj['team']
                team = Team.objects.get(id=team_id)
                obj['team'] = team
                obj['rank'] = idx
                ranked_queryset.append(obj)

            # 로그인 상태에 따라 my_team_ranking 정보를 다르게 설정
            my_team_ranking = None
            if request.user.is_authenticated:
                my_team = request.user.team
                my_team_ranking = next((obj for obj in ranked_queryset if obj['team'] == my_team), None)
                if my_team_ranking:
                    serializer = TeamRankingSerializer(my_team_ranking)
                    my_team_ranking = [serializer.data]
                else:
                    return Response({"detail": "참가한 대회가 없습니다."}, status=status.HTTP_200_OK)
            else:
                my_team_ranking = '로그인이 필요합니다.'

            return Response(my_team_ranking, status=status.HTTP_200_OK)

        except NotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)