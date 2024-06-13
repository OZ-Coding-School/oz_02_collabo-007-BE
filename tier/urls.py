from django.urls import path
from .views import TierListView

urlpatterns = [
    path('tiers/all/', TierListView.as_view(), name='tier-list')
]