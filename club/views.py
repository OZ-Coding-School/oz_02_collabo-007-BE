from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Club
from users.models import CustomUser
from team.models import Team
from coach.models import Coach
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
                    ClubListSerializer,
                    ClubDetailSerializer,
                    CoachSerializer,
                    TeamSerializer,
                    UserWithTeamInfoSerializer
)


# 클럽 목록 조회 API (회원가입 전용)
class ClubListView(APIView):
    """
    클럽 목록 조회 API (회원가입 때 이용)
    """
    @swagger_auto_schema(
        operation_summary='클럽 목록 조회 (회원가입 때 사용)',
        operation_description='클럽 목록 조회 API (회원가입 때 이용)',
    )
    
    def get(self, request):
        try:
            # is_deleted=False를 사용하여 삭제되지 않은 클럽만 조회
            clubs = Club.objects
            serializer = ClubListSerializer(clubs, many=True)
            # 성공 시 성공 메세지와 함께 데이터 반환
            return Response({
                'code': '200',
                "message": "클럽 목록 조회 성공",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception:
            # 예외 발생 시 단순한 에러 메세지 반환
            return Response({
                "code": "500",
                "message": "클럽 목록 조회 중 오류발생"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            

# 클럽 상세 정보 조회 API
class ClubDetailView(APIView):
    """
    클럽 상세 정보 조회하는 API
    """
    @swagger_auto_schema(
        operation_summary='클럽 상세 정보 조회',
        operation_description='클럽 상세 정보 조회하는 API',
    )
    
    def get(self, request, pk):
        try:
            club = Club.objects.get(pk=pk)
            club_serializer = ClubDetailSerializer(club)

            # 클럽에 속한 코치 정보 가져오기
            coaches = Coach.objects.filter(club=club)
            coach_serializer = CoachSerializer(coaches, many=True)
            
            # 클럽에 속한 팀 정보 가져오기
            teams = Team.objects.filter(club=club)
            team_serializer = TeamSerializer(teams, many=True)
            
            
            # 클럽에 속한 코치들의 유저 ID 목록 가져오기
            # values_list => 특정 필드의 값을 리스트 형태로 가져올 때 사용
            # flat=True => 하나의 필드를 불러올 때 True 값을 줘서 튜플형태가 아닌 단일 값으로 가져온다
            coaches_users_ids = coaches.values_list('user', flat=True) 
            

            # 클럽에 속한 상위 3명 유저 정보 가져오기 (코치로 등록된 유저 제외)
            users = CustomUser.objects.filter(club=club).exclude(id__in=coaches_users_ids).order_by('username')[:3] # 추후에 order_by('-score')[:3] 으로 변경
            user_serializer = UserWithTeamInfoSerializer(users, many=True)

            # 클럽 정보와 함께 코치, 팀, 유저 정보 포함하여 응답
            response_data = {
                'club': club_serializer.data,
                'coaches': coach_serializer.data,
                'teams': team_serializer.data,
                'users': user_serializer.data
            }
            
            return Response(response_data)
        except Club.DoesNotExist:
            return Response({'error': '해당클럽이 존재하지 않습니다.'}, status=404)
        
        
        

        
class ClubUsersListView(APIView):
    """
    클럽에 속한 유저 정보를 모두 나타내는 API
    """
    @swagger_auto_schema(
        operation_summary='클럽에 속한 유저 정보 조회',
        operation_description='클럽에 속한 유저 정보를 모두 나타내는 API',
    )
    
    def get(self, request, pk):
        try:
            # 클럽 객체 가져오기
            club = Club.objects.get(pk=pk)
            
            # 클럽에 속한 코치들의 유저 ID 목록 가져오기
            coaches = Coach.objects.filter(club=club)
            coaches_users_ids = coaches.values_list('user', flat=True)
            
            # 클럽에 속한 유저 정보 가져오기 (코치로 등록된 유저 제외)
            users = CustomUser.objects.filter(club=club).exclude(id__in=coaches_users_ids).order_by('username')
            user_serializer = UserWithTeamInfoSerializer(users, many=True)

            # 유저 정보 포함하여 응답
            return Response(user_serializer.data)
        except Club.DoesNotExist:
            return Response({'error': '해당 클럽이 존재하지 않습니다.'}, status=404)