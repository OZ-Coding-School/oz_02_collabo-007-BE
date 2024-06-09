import random
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from applicant_info.models import ApplicantInfo
from competition.models import Competition
from custom_admin.competition.serializers import ApplicantInfoSerializer, CompetitionListSerializer, CompetitionSerializer, MatchResultSerializer, MatchSerializer, ParticipantInfoSerializer
from custom_admin.pagination import StandardResultsSetPagination
from custom_admin.service.competition_service import CompetitionService
from custom_admin.service.image_service import ImageService
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Prefetch, Exists, OuterRef
from match.models import Match
from participant.models import Participant
from participant_info.models import ParticipantInfo
from payments.models import Payment


class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all().select_related(
        'image_url', 'tier', 'match_type').order_by('-created_at')
    pagination_class = StandardResultsSetPagination
    image_service = ImageService()
    competition_service = CompetitionService()

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

    @swagger_auto_schema(
        operation_summary='대회 상세 조회',
        operation_description='대회 상세 정보를 조회합니다.',
        responses={
            200: CompetitionSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='대회 생성',
        operation_description='대회를 생성합니다.',
        responses={
            201: CompetitionSerializer,
            400: 'Bad Request',
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            match_type = validated_data.get('match_type')
            tier = validated_data.get('tier')

            competition = Competition.objects.create(
                name=validated_data.get('name'),
                description=validated_data.get('description'),
                start_date=validated_data.get('start_date'),
                end_date=validated_data.get('end_date'),
                status='before',
                total_rounds=validated_data.get('total_rounds'),
                total_sets=validated_data.get('total_sets'),
                rule=validated_data.get('rule'),
                address=validated_data.get('address'),
                location=validated_data.get('location'),
                code=self._make_competition_code(),
                phone=validated_data.get('phone'),
                fee=validated_data.get('fee'),
                bank_name=validated_data.get('bank_name'),
                bank_account_number=validated_data.get('bank_account_number'),
                bank_account_name=validated_data.get('bank_account_name'),
                site_link=validated_data.get('site_link'),
                match_type=match_type,
                tier=tier,
                max_participants=self._get_max_participants(
                    validated_data.get('competition_type'),
                    validated_data.get('total_rounds'),
                    validated_data.get('max_participants')
                ),
                deposit_date=validated_data.get('deposit_date'),
                competition_type=validated_data.get('competition_type')
            )

            image_data = request.data.get('image_file')
            if image_data:
                self.image_service.upload_image(competition, image_data)

            return Response(CompetitionSerializer(competition).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e.with_traceback())
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def _make_competition_code(self):
        code = random.randint(100000, 999999)
        return code

    def _get_max_participants(self, competition_type, total_rounds, max_participants):
        if competition_type == 'tournament':
            return pow(2, total_rounds)
        return max_participants if max_participants > 0 else None

    @swagger_auto_schema(
        operation_summary='대회 참가자 목록 조회',
        operation_description='대회 참가자 목록을 조회합니다.',
        responses={
            200: ApplicantInfoSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['get'], url_path='applicants', url_name='competition-applicants')
    def applicants(self, request, pk=None):
        competition = self.get_object()
        payments = Payment.objects.filter(applicant_info=OuterRef('pk'))
        refunds = Payment.objects.filter(
            applicant_info=OuterRef('pk'), refund__isnull=False)

        applicant_infos = ApplicantInfo.objects.filter(
            competition=competition
        ).prefetch_related(
            Prefetch('applicants__user'),
            Prefetch('payment__refund')
        ).annotate(
            has_payment=Exists(payments),
            has_refund=Exists(refunds)
        )

        serializer = ApplicantInfoSerializer(applicant_infos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='입금 처리',
        operation_description='사용자의 입금을 처리합니다.',
        responses={
            200: 'Payment processed successfully',
            400: 'Bad Request',
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['post'], url_path=r'applicants/(?P<applicant_id>\d+)/payment', url_name='process-payment')
    def process_user_payment(self, request, * args, **kwargs):
        try:
            applicant_id = kwargs.get('applicant_id')
            applicant_info = ApplicantInfo.objects.get(pk=applicant_id)
            self.competition_service.process_payment(applicant_info)
        except ApplicantInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response('입금 확인이 완료되었습니다.', status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='신청 취소',
        operation_description='사용자의 대회 신청을 취소합니다.',
        responses={
            200: 'Application canceled successfully',
            400: 'Bad Request',
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['post'], url_path=r'applicants/(?P<applicant_id>\d+)/cancel', url_name='cancel-application')
    def cancel_user_application(self, request, *args, **kwargs):
        try:
            applicant_id = kwargs.get('applicant_id')
            applicant_info = ApplicantInfo.objects.get(pk=applicant_id)
            if applicant_info.is_canceled():
                return Response('이미 취소된 신청입니다.', status=status.HTTP_400_BAD_REQUEST)

            self.competition_service.cancel_application(applicant_info)
        except ApplicantInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response('신청이 취소되었습니다.', status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='환불 처리',
        operation_description='사용자의 환불을 처리합니다.',
        responses={
            200: 'Refund processed successfully',
            400: 'Bad Request',
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['post'], url_path=r'applicants/(?P<applicant_id>\d+)/refund', url_name='process-refund')
    def process_user_refund(self, request, *args, **kwargs):
        try:
            applicant_id = kwargs.get('applicant_id')
            applicant_info = ApplicantInfo.objects.get(pk=applicant_id)
            self.competition_service.process_refund(applicant_info)
        except ApplicantInfo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response('환불이 완료되었습니다.', status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='대회 참가자 목록 조회',
        operation_description='대회 참가자 목록을 조회합니다.',
        responses={
            200: ApplicantInfoSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['get'], url_path='participants', url_name='competition-participants')
    def participants(self, request, pk=None):
        competition = self.get_object()
        participant_infos = ParticipantInfo.objects.filter(
            competition=competition
        ).prefetch_related(
            Prefetch('participants__user')
        )

        serializer = ParticipantInfoSerializer(participant_infos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='get',
        operation_summary='대회 경기 목록 조회',
        operation_description='대회 경기 목록을 조회합니다.',
        responses={
            200: MatchSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @swagger_auto_schema(
        method='post',
        operation_summary='대회 경기 생성',
        operation_description='대회 경기를 생성합니다.',
        responses={
            201: MatchSerializer,
            400: 'Bad Request',
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['get', 'post'], url_path='matches', url_name='competition-matches')
    def matches(self, request, pk=None):
        if request.method == 'POST':
            try:
                competition = self.get_object()
                request.data['competition'] = competition.id
                request.data['total_sets'] = competition.total_sets
                serializer = MatchSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                if serializer.validated_data['a_team'] == serializer.validated_data['b_team']:
                    return Response('동일한 팀은 경기를 할 수 없습니다.', status=status.HTTP_400_BAD_REQUEST)

                result = self.competition_service.create_match(
                    serializer.validated_data)
                return Response(MatchSerializer(result).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            competition = self.get_object()
            matches = Match.objects.filter(competition=competition).select_related(
                'a_team', 'b_team', 'winner_id'
            ).prefetch_related(
                'a_team__participants', 'b_team__participants', 'winner_id__participants', 'a_team__participants__user', 'b_team__participants__user', 'winner_id__participants__user'
            )

            serializer = MatchSerializer(matches, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='대회 경기 상세 조회',
        operation_description='대회 경기 상세 정보를 조회합니다.',
        responses={
            200: MatchResultSerializer,
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['get'], url_path=r'matches/(?P<match_id>\d+)', url_name='competition-match')
    def match(self, request, *args, **kwargs):
        match_id = kwargs.get('match_id')
        match = Match.objects.select_related(
            'a_team', 'b_team'
        ).prefetch_related(
            Prefetch('a_team__participants',
                     queryset=Participant.objects.select_related('user')),
            Prefetch('b_team__participants',
                     queryset=Participant.objects.select_related('user')),
            'set_list'
        ).get(pk=match_id)

        serializer = MatchResultSerializer(match)
        return Response(serializer.data, status=status.HTTP_200_OK)
