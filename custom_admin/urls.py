from django.urls import path, include

app_name = 'custom_admin'
urlpatterns = [
    path('admin/users/', include('custom_admin.user.urls')),
    path('admin/', include('custom_admin.club.urls')),
    path('admin/', include('custom_admin.team.urls')),
]
