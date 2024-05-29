from .views import (CompetitionViewSet,)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'competitions', CompetitionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
