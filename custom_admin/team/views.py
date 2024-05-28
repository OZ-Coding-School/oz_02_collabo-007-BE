from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from custom_admin.team.serializers import TeamDetailSerializer, MemberSerializer
from team.models import Team
from custom_admin.service.image_service import ImageService
from drf_yasg.utils import swagger_auto_schema


class TeamViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = TeamDetailSerializer
    image_service = ImageService()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Team.objects.none()
        return Team.objects.all()

    @swagger_auto_schema(
        operation_summary='팀 상세 조회',
        operation_description='팀 상세 정보를 조회합니다.',
        responses={
            200: TeamDetailSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='팀 수정',
        operation_description='팀 정보를 수정합니다.',
        responses={
            200: TeamDetailSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            400: 'Bad Request'
        }
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        image_data = serializer.validated_data.pop('image_file', None)
        delete_image = serializer.validated_data.get('delete_image', False)

        if delete_image:
            self.image_service.delete_image(instance)

        if image_data and hasattr(image_data, 'size') and image_data.size > 0:
            self.image_service.upload_image(instance, image_data)

        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(
        method='get',
        operation_summary='멤버 목록 조회',
        operation_description='팀의 멤버 목록을 조회합니다.',
        responses={
            200: TeamDetailSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['get'], url_path='members')
    def members(self, request, *args, **kwargs):
        team = self.get_object()
        return Response(MemberSerializer(team.users.all(), many=True).data, status=status.HTTP_200_OK)
