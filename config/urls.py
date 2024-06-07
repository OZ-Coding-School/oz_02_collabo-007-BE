from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Alchemist tennis Swagger',
        default_version='dev v1',
        description='',
        terms_of_service=".",
        contact=openapi.Contact(email="o@o.com"),
        license=openapi.License(name="By. 지돌이")
    ),
    public=True,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')), # include를 활용하여 각 독립적인app의 urls.py 를 포함 시킴
    path('api/v1/', include('club.urls')),
    path('api/v1/', include('team.urls')),
    path('api/v1/', include('competition.urls')),
    path('api/v1/', include('point.urls')),
    path('api/v1/', include('match.urls')),
    path('api/v1/', include('custom_admin.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')]
