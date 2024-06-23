from custom_admin.auth.views import AdminLoginView, AdminRefreshView
from django.urls import path


urlpatterns = [
    path('login/', AdminLoginView.as_view(), name='login'),
    path('refresh/', AdminRefreshView.as_view(), name='refresh')
]
