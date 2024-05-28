from .views import (ClubViewSet,)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'clubs', ClubViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
