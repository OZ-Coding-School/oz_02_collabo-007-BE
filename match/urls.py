from django.urls import path
from .views import MatchRoundAPIView

urlpatterns = [
    path('competitions/<int:competition_id>/status/', MatchRoundAPIView.as_view(), name='competitions_status'),
]
