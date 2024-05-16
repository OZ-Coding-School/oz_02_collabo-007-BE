from django.urls import path, include

app_name = 'custom_admin'
urlpatterns = [
    path('admin/users/', include('custom_admin.users.urls')),
]
