
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from custom_admin.service.competition_service import CompetitionService
from match.models import Match
from matchtype.models import MatchType
from tier.models import Tier
from .serializers import AddPointsSerializer, AddTeamPointsSerializer, MatchDetailSerializer, TeamMatchDetailSerializer
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

    @swagger_auto_schema(
        operation_summary='팀 경기 결과 입력',
        operation_description='팀 경기 결과를 입력합니다.',
        responses={
            200: '경기 결과 입력 성공',
            401: 'Authentication Error',
            403: 'Permission Denied',
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['post'], url_path='team/result', url_name='team-match-result')
    def team_match_result(self, request, *args, **kwargs):
        try:
            serializer = TeamMatchDetailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            match_id = kwargs.get('pk')
            match = self.competition_service.update_or_create_team_match_result(
                match_id=match_id, match_data=request.data)
            return Response('시합 결과를 저장했습니다.', status=status.HTTP_200_OK)
        except Exception as e:
            print(e.with_traceback())
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post',
        operation_summary='경기 포인트 추가',
        operation_description='경기에 포인트를 추가합니다.',
        request_body=AddPointsSerializer,
        responses={
            200: '포인트 추가 성공',
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['post'], url_path='points', url_name='add-points')
    def add_points(self, request, *args, **kwargs):
        try:
            serializer = AddPointsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            match_id = kwargs.get('pk')
            self.competition_service.add_points_to_match(
                match_id, serializer.validated_data)

            return Response('포인트가 성공적으로 추가되었습니다.', status=status.HTTP_200_OK)
        except Match.DoesNotExist:
            return Response('경기를 찾을 수 없습니다.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response('포인트를 추가하지 못했습니다.', status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post',
        operation_summary='팀 경기 포인트 추가',
        operation_description='팀 경기에 포인트를 추가합니다.',
        request_body=AddPointsSerializer,
        responses={
            200: '포인트 추가 성공',
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['post'], url_path='team/points', url_name='add-team-points')
    def add_team_points(self, request, *args, **kwargs):
        try:
            serializer = AddTeamPointsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            match_id = kwargs.get('pk')
            self.competition_service.add_points_to_team_match(
                match_id, serializer.validated_data)

            return Response('포인트가 성공적으로 추가되었습니다.', status=status.HTTP_200_OK)
        except Match.DoesNotExist:
            return Response('경기를 찾을 수 없습니다.', status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
