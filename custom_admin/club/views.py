from club.models import Club
from custom_admin.club.serializers import ClubListSerializer, ClubSerializer, MemberSerializer, TeamSerializer, User
from custom_admin.pagination import StandardResultsSetPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, permission_classes, authentication_classes
from custom_admin.service.image_service import ImageService
from rest_framework.response import Response

from team.models import Team


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all().order_by('-created_at')
    pagination_class = StandardResultsSetPagination
    image_service = ImageService()

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        club = Club.objects.create(
            name=serializer.validated_data['name'],
            description=serializer.validated_data['description'],
            address=serializer.validated_data['address'],
            phone=serializer.validated_data['phone']
        )

        image_data = request.data.get('image_file')
        if image_data:
            self.image_service.upload_image(club, image_data)

        return Response(ClubSerializer(club).data, status=status.HTTP_201_CREATED)

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

        return Response(ClubSerializer(instance).data, status=status.HTTP_200_OK)

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

    @swagger_auto_schema(
        method='get',
        operation_summary='팀 목록 조회',
        operation_description='클럽에 속한 팀 목록을 조회합니다.',
        responses={
            200: TeamSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @swagger_auto_schema(
        method='post',
        operation_summary='팀 생성',
        operation_description='클럽에 속한 팀을 생성합니다.',
        request_body=TeamSerializer,
        responses={
            201: TeamSerializer,
            400: 'Bad Request',
            401: 'Authentication Error',
            403: 'Permission Denied',
        }
    )
    @action(detail=True, methods=['get', 'post'], url_name='teams', url_path='teams')
    def teams(self, request, *args, **kwargs):
        club = self.get_object()

        if request.method == 'GET':
            return Response(TeamSerializer(club.teams.all(), many=True).data, status=status.HTTP_200_OK)

        if request.method == 'POST':
            return self._create_team(request, club)

    def _create_team(self, request, club):
        try:
            request.data['club'] = club.id
            serializer = TeamSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            team = Team.objects.create(
                name=serializer.validated_data['name'],
                club=club,
                description=serializer.validated_data['description']
            )

            image_data = request.data.get('image_file')
            if image_data:
                self.image_service.upload_image(team, image_data)

            return Response(TeamSerializer(team).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e.with_traceback())
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='get',
        operation_summary='멤버 목록 조회',
        operation_description='클럽에 속한 멤버 목록을 조회합니다.',
        responses={
            200: MemberSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @swagger_auto_schema(
        method='put',
        operation_summary='멤버 수정',
        operation_description='클럽 멤버의 팀을 수정합니다.',
        responses={
            200: MemberSerializer,
            400: 'Bad Request',
            401: 'Authentication Error',
            403: 'Permission Denied',
        }
    )
    @action(detail=True, methods=['get', 'put'], url_name='members', url_path='members')
    def members(self, request, *args, **kwargs):
        club = self.get_object()

        if request.method == 'GET':
            return Response(MemberSerializer(User.objects.filter(club=club), many=True).data, status=status.HTTP_200_OK)

        if request.method == 'PUT':
            return self._update_member(request)

    def _update_member(self, request):
        try:
            user = User.objects.get(pk=request.data['user_id'])
            user.team_id = request.data['team_id']
            user.save()
            return Response(MemberSerializer(user).data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
