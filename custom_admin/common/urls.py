from .views import TierViewSet, MatchTypeViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'common/tiers', TierViewSet)
router.register(r'common/matchtypes', MatchTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
