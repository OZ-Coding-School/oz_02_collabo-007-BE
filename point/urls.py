from django.urls import path
from .views import UserRankingView, TeamRankingView, RealtimeMyRankingView, RealtimeMyTeamRankingView

urlpatterns = [
    path('ranking/user/', UserRankingView.as_view(), name='user_ranking'),
    path('ranking/team/', TeamRankingView.as_view(), name='team_ranking'),
    path('ranking/realtime/myrank/', RealtimeMyRankingView.as_view(), name='realtime_my_ranking'),
    path('ranking/realtime/myteamrank/', RealtimeMyTeamRankingView.as_view(), name='realtime_my_team_ranking'),
    
]