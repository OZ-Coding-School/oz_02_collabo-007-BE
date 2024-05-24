from .views import (ClubViewSet, MemberViewSet, TeamViewSet,)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

router = DefaultRouter()
router.register(r'clubs', ClubViewSet)

# Create a nested router
clubs_router = NestedDefaultRouter(router, r'clubs', lookup='club')
clubs_router.register(r'teams', TeamViewSet, basename='club-teams')
clubs_router.register(r'members', MemberViewSet, basename='club-members')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(clubs_router.urls)),
]
