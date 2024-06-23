from custom_admin.auth.views import AdminLoginView
from django.urls import path


urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='login'),
]
