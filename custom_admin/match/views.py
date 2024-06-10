
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from custom_admin.service.competition_service import CompetitionService
from match.models import Match
from .serializers import MatchDetailSerializer
from drf_yasg.utils import swagger_auto_schema


class MatchViewSet(viewsets.GenericViewSet):
    serializer_class = MatchDetailSerializer
    competition_service = CompetitionService()

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Match.objects.none()
        return Match.objects.all().select_related('competition', 'winner')

    @swagger_auto_schema(
        operation_summary='경기 결과 입력',
        operation_description='경기 결과를 입력합니다.',
        responses={
            200: '경기 결과 입력 성공',
            401: 'Authentication Error',
            403: 'Permission Denied',
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['post'], url_path='result', url_name='match-result')
    def post(self, request, *args, **kwargs):
        try:
            serializer = MatchDetailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            match_id = kwargs.get('pk')
            match = self.competition_service.update_or_create_match_result(
                match_id=match_id, match_data=request.data)
            return Response('시합 결과를 저장했습니다.', status=status.HTTP_200_OK)
        except Exception as e:
            print(e.with_traceback())
            return Response('시합 결과를 저장하지 못했습니다.', status=status.HTTP_400_BAD_REQUEST)
