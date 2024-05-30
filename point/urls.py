from django.urls import path
from .views import LiveRankingView

urlpatterns = [
    path('live-ranking/', LiveRankingView.as_view(), name='live-ranking'),
]