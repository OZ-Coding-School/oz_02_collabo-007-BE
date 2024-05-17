from django.urls import path
from .views import (UserViewSet,)
from rest_framework import routers

user_list = UserViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
    # path('', user_list, name='user-list'),
]

router = routers.SimpleRouter()
router.register('', UserViewSet)

urlpatterns += router.urls