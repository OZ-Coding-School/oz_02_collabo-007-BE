from django.urls import path
from .views import RealtimeUserRankingView, RealtimeTeamRankingView, RealtimeMyRankingView, RealtimeMyTeamRankingView

urlpatterns = [
    path('ranking/realtime/user', RealtimeUserRankingView.as_view(), name='realtime_user_ranking'),
    path('ranking/realtime/team', RealtimeTeamRankingView.as_view(), name='realtime_team_ranking'),
    path('ranking/realtime/myrank', RealtimeMyRankingView.as_view(), name='realtime_my_ranking'),
    path('ranking/realtime/myteamrank', RealtimeMyTeamRankingView.as_view(), name='realtime_my_team_ranking'),
    
]