from django.urls import path
from .views import MatchRoundAPIView, MatchRecordAPIView

urlpatterns = [
    path('competitions/<int:competition_id>/status/', MatchRoundAPIView.as_view(), name='competitions_status'),
    path('competitions/record/', MatchRecordAPIView.as_view(), name='record'),
]
