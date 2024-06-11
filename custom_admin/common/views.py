from rest_framework import viewsets, mixins

from custom_admin.common.serializers import AdminMatchTypeSerializer, AdminTierSerializer
from matchtype.models import MatchType
from tier.models import Tier
from drf_yasg.utils import swagger_auto_schema


class TierViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tier.objects.all().select_related('match_type')
    serializer_class = AdminTierSerializer

    @swagger_auto_schema(
        operation_summary='부 목록 조회',
        operation_description='부 목록을 조회합니다.',
        responses={
            200: AdminTierSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MatchTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = MatchType.objects.all()
    serializer_class = AdminMatchTypeSerializer

    @swagger_auto_schema(
        operation_summary='경기 타입 목록 조회',
        operation_description='경기 타입 목록을 조회합니다.',
        responses={
            200: AdminMatchTypeSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
