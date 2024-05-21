from django.urls import path
from .views import (UserViewSet,)
from rest_framework import routers


urlpatterns = [

]

router = routers.SimpleRouter()
router.register('', UserViewSet)

urlpatterns += router.urls
