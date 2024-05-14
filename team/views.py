from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team
from users.models import CustomUser
from .serializers import TeamDetailSerializer
from club.serializers import UserWithTeamInfoSerializer

class TeamDetailView(APIView):
    """
    팀 상세 정보 조회하는 API
    """
    def get(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
            team_serializer = TeamDetailSerializer(team)

            # 팀에 속한 상위 3명 유저 정보 가져오기
            users = CustomUser.objects.filter(team=team).order_by('id')[:3] # 추후에 order_by('-score')[:3] 으로 변경
            user_serializer = UserWithTeamInfoSerializer(users, many=True)

            
            response_data = {
                'team': team_serializer.data,
                'users': user_serializer.data
            }
            
            return Response(response_data)
        except Team.DoesNotExist:
            return Response({'error': '해당팀이 존재하지 않습니다.'}, status=404)
        
        
        
class TeamUsersListView(APIView):
    """
    팀에 속한 유저 정보를 모두 나타내는 API
    """
    def get(self, request, pk):
        try:
            # 클럽 객체 가져오기
            team = Team.objects.get(pk=pk)
            
            # 클럽에 속한 유저 정보 가져오기
            users = CustomUser.objects.filter(team=team).order_by('id')
            user_serializer = UserWithTeamInfoSerializer(users, many=True)

            # 유저 정보 포함하여 응답
            return Response(user_serializer.data)
        except Team.DoesNotExist:
            return Response({'error': '해당 팀이 존재하지 않습니다.'}, status=404)
        
        
        
        

