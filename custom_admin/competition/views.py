from rest_framework import viewsets
from competition.models import Competition
from custom_admin.competition.serializers import CompetitionListSerializer, CompetitionSerializer
from custom_admin.pagination import StandardResultsSetPagination
from custom_admin.service.image_service import ImageService
from drf_yasg.utils import swagger_auto_schema


class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all().select_related(
        'image_url', 'tier', 'match_type').order_by('-created_at')
    pagination_class = StandardResultsSetPagination
    image_service = ImageService()

    def get_serializer_class(self):
        if self.action == 'list':
            return CompetitionListSerializer
        return CompetitionSerializer

    @swagger_auto_schema(
        operation_summary='대회 목록 조회',
        operation_description='대회 목록을 조회합니다.',
        responses={
            200: CompetitionSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
