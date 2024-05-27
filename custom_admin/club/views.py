from club.models import Club
from custom_admin.club.serializers import ClubListSerializer, ClubSerializer, MemberSerializer, TeamSerializer, User
from custom_admin.pagination import StandardResultsSetPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, exceptions, mixins, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, permission_classes, authentication_classes

from team.models import Team


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all().order_by('-created_at')
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ClubListSerializer
        return ClubSerializer

    @swagger_auto_schema(
        operation_summary='클럽 목록 조회',
        operation_description='클럽 목록을 조회합니다.',
        responses={
            200: ClubSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='클럽 상세 조회',
        operation_description='클럽 상세 정보를 조회합니다.',
        responses={
            200: ClubSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='클럽 생성',
        operation_description='클럽을 생성합니다.',
        responses={
            201: ClubSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            400: 'Bad Request'
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='클럽 수정',
        operation_description='클럽 정보를 수정합니다.',
        responses={
            200: ClubSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            400: 'Bad Request'
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='클럽 삭제',
        operation_description='클럽을 삭제합니다.',
        responses={
            204: 'No Content',
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class TeamViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = TeamSerializer

    @swagger_auto_schema(
        operation_summary='팀 목록 조회',
        operation_description='팀 목록을 조회합니다.',
        responses={
            200: TeamSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # Return an empty queryset or a mock queryset during schema generation
            return Team.objects.none()

        return Team.objects.filter(club=self.kwargs['club_pk'])

    @swagger_auto_schema(
        operation_summary='팀 생성',
        operation_description='팀을 생성합니다.',
        responses={
            201: TeamSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            400: 'Bad Request'
        }
    )
    def create(self, request, *args, **kwargs):
        club = Club.objects.get(pk=self.kwargs['club_pk'])
        if not club:
            raise exceptions.NotFound('Club not found')
        request.data['club'] = club.pk
        return super().create(request, *args, **kwargs)


class MemberViewSet(mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = MemberSerializer

    @swagger_auto_schema(
        operation_summary='클럽 회원 목록 조회',
        operation_description='클럽 회원 목록을 조회합니다.',
        responses={
            200: MemberSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return User.objects.none()

        return User.objects.filter(club=self.kwargs['club_pk'])

    @swagger_auto_schema(
        operation_summary='클럽 회원 정보 수정',
        operation_description='클럽 회원 정보를 수정합니다.',
        responses={
            200: MemberSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            400: 'Bad Request'
        }
    )
    def update(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        if not user:
            raise exceptions.NotFound('User not found')
        return super().update(request, *args, **kwargs)
