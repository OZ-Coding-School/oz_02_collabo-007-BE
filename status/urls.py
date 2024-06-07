from django.urls import path
from .views import MatchRoundAPIView

urlpatterns = [
    path('status/match/round', MatchRoundAPIView.as_view(), name='match_round_status'),
]

