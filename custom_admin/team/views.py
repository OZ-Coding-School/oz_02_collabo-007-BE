from rest_framework import viewsets, mixins
from custom_admin.team.serializers import TeamDetailSerializer
from drf_yasg.utils import swagger_auto_schema

from team.models import Team


class TeamViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = TeamDetailSerializer

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
        return super().update(request, *args, **kwargs)
