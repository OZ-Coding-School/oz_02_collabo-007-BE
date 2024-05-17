from users.models import CustomUser
from custom_admin.users.serializers import UserSerializer
from custom_admin.pagination import StandardResultsSetPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, exceptions, mixins, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, permission_classes, authentication_classes


# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated, IsAdminUser])
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        operation_summary='어드민 유저 목록 조회',
        operation_description='어드민 유저 목록을 조회합니다.',
        responses={
            200: UserSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='어드민 유저 상세 조회',
        operation_description='어드민 유저 상세 정보를 조회합니다.',
        responses={
            200: UserSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='어드민 유저 정보 수정',
        operation_description='어드민 유저 정보를 수정합니다.',
        responses={
            200: UserSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='어드민 유저 삭제',
        operation_description='어드민 유저를 삭제합니다.',
        responses={
            204: 'No Content',
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='어드민 유저 생성',
        operation_description='어드민 유저를 생성합니다.',
        responses={
            201: UserSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
