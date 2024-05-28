from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from users.models import CustomUser
from custom_admin.user.serializers import UserSerializer
from custom_admin.pagination import StandardResultsSetPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from custom_admin.service.image_service import ImageService

User = get_user_model()
INITIAL_PASSWORD = '123456'

# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated, IsAdminUser])


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    image_service = ImageService()

    @swagger_auto_schema(
        operation_summary='어드민 유저 목록 조회',
        operation_description='어드민 유저 목록을 조회합니다.',
        responses={
            200: UserSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='어드민 유저 상세 조회',
        operation_description='어드민 유저 상세 정보를 조회합니다.',
        responses={200: UserSerializer,
                   401: 'Authentication Error',
                   403: 'Permission Denied',
                   404: 'Not Found'}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='어드민 유저 생성',
        operation_description='관리자가 유저를 생성합니다.',
        responses={201: UserSerializer, 400: 'Bad Request'}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            club = serializer.validated_data.get('club')
            user = User.objects.create_user(
                phone=serializer.validated_data['phone'],
                password=INITIAL_PASSWORD,
                username=serializer.validated_data['username'],
                birth=serializer.validated_data.get('birth'),
                gender=serializer.validated_data.get('gender'),
                club=club
            )

            image_data = request.data.get('image_file')
            if image_data:
                self.image_service.upload_image(user, image_data)

            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e.with_traceback())
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='어드민 유저 수정',
        operation_description='관리자가 유저 정보를 수정합니다.',
        responses={200: UserSerializer, 400: 'Bad Request'}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        for attr, value in serializer.validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        image_data = request.data.get('image_file')
        delete_image = request.data.get('delete_image', False)

        if delete_image:
            self.image_service.delete_image(instance)

        if image_data and hasattr(image_data, 'size') and image_data.size > 0:
            self.image_service.upload_image(instance, image_data)

        return Response(UserSerializer(instance).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='어드민 유저 삭제',
        operation_description='관리자가 유저를 삭제합니다.',
        responses={204: 'No Content',  401: 'Authentication Error',
                   403: 'Permission Denied', 404: 'Not Found'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
