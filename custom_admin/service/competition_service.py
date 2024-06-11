from django.shortcuts import get_object_or_404
from applicant_info.models import ApplicantInfo
from django.db import transaction
from competition.models import Competition
from matchtype.models import MatchType
from participant.models import Participant
from participant_info.models import ParticipantInfo
from payments.models import Payment, Refund
from match.models import Match
from point.models import Point
from tier.models import Tier
from users.models import CustomUser


class CompetitionService:
    def process_payment(self, applicant_info: ApplicantInfo):
        """
        관리자가 대회 신청자의 결제를 확인했을 때 호출되는 메서드.
        """
        with transaction.atomic():
            applicant_info = self._confirm_payment(applicant_info)
            if applicant_info.is_confirmed():
                self._create_participant(applicant_info)
        return None

    def cancel_application(self, applicant_info: ApplicantInfo):
        """
        관리자가 대회 신청자의 신청을 취소했을 때 호출되는 메서드.
        """
        with transaction.atomic():
            self._cancel_application(applicant_info)
        return None

    def process_refund(self, applicant_info: ApplicantInfo):
        """
        관리자가 대회 신청자의 환불을 처리했을 때 호출되는 메서드.
        """
        with transaction.atomic():
            payment = Payment.objects.get(applicant_info=applicant_info)
            if payment is None:
                return None
            Refund.objects.create(payment=payment)
        return None

    def create_match(self, match_data):
        """
        대회의 경기를 생성하는 메서드.
        """
        with transaction.atomic():
            # TODO: 토너먼트일 경우, 라운드와 경기 번호가 중복되지 않도록 처리
            # TODO: 토너먼트일 경우, 라운드 수가 총 라운드 수를 넘지 않도록 처리
            match = Match.objects.create(**match_data)

        return match

    def edit_match(self, match: Match, match_data):
        """
        대회의 경기를 수정하는 메서드.
        """
        with transaction.atomic():
            for attr, value in match_data.items():
                setattr(match, attr, value)
            match.save()

        return match

    def update_or_create_match_result(self, match_id, match_data):
        """
        경기 결과를 입력하거나 수정하는 메서드.
        """
        with transaction.atomic():
            match = get_object_or_404(Match, id=match_id)

            for set_data in match_data['sets']:
                self._create_or_update_set(match, set_data)

            winner = match_data.get('winner')
            if winner == 'a':
                match.winner_id = match.a_team
            if winner == 'b':
                match.winner_id = match.b_team
            if winner is None or winner == '':
                match.winner_id = None

            match.save()

        return match

    def add_points_to_match(self, match_id, points_data):
        """
        승점을 추가하는 메서드.

        Args:
            match_id: Match 객체의 id
            points_data: AddPointsSerializer로 직렬화된 데이터
            e.g. {
                'points_array': [
                    {
                        'points': 10,
                        'expired_date': '2021-12-31',
                        'user_id': 1
                    },
                    {
                        'points': 20,
                        'expired_date': '2021-12-31',
                        'user_id': 2
                    }
                ],
                'tier_id': 1,
                'match_type_id': 1
            }
        """
        with transaction.atomic():
            match = get_object_or_404(Match, id=match_id)

            tier = self._get_object_or_404(Tier, pk=points_data.get('tier_id'))
            match_type = self._get_object_or_404(
                MatchType, pk=points_data.get('match_type_id'))

            points_array = points_data['points_array']

            for point_entry in points_array:
                user = self._get_object_or_404(
                    CustomUser, pk=point_entry.get('user_id'))
                self._create_point(match, user, point_entry, tier, match_type)

        return None

    def _confirm_payment(self, applicant_info: ApplicantInfo):
        """
        참가자가 입금 완료했을 때 호출되는 메서드.

        이 메서드는 다음 작업을 수행합니다:
        1. 결제 정보를 생성합니다.
        2-1. 대기번호가 있는 경우 상태를 '참가 대기중'으로 변경합니다.
        2-2. 대기번호가 없는 경우 상태를 '참가 완료'로 변경합니다.

        Args:
            applicant_info: ApplicantInfo 객체

        Returns:
            applicant_info: 업데이트된 ApplicantInfo 객체
        """
        Payment.objects.create(applicant_info=applicant_info)

        if applicant_info.waiting_number is None:
            applicant_info.change_status_to_confirmed()
        else:
            applicant_info.change_status_to_pending()

        return applicant_info

    def _create_participant(self, applicant_info: ApplicantInfo):
        """
        대회 신청자가 대회 참가 상태로 변경될 때 참가자 정보를 생성하는 메서드.

        이 메서드는 다음 작업을 수행합니다:
        1. 신청자 정보에 등록된 사용자 정보를 참가자 정보로 생성합니다.

        Args:
            applicant_info: ApplicantInfo 객체

        Returns:
            participant_info: 생성된 ParticipantInfo 객체
        """
        participant_info = ParticipantInfo.objects.create(
            competition=applicant_info.competition, applicant_info=applicant_info)

        users = applicant_info.get_users()

        for user in users:
            Participant.objects.create(
                user=user,
                participant_info=participant_info
            )

        return participant_info

    def _cancel_application(self, applicant_info: ApplicantInfo):
        """
        참가자의 신청을 취소하는 메서드.

        이 메서드는 다음 작업을 수행합니다:
        1. 참가자 정보에 연결된 참가자 정보를 삭제합니다.
        2. 삭제된 참가자 정보가 있을 경우, 참가 대기 중인 참가자 중 가장 높은 대기번호를 찾아 참가 정보를 생성합니다.
        3. 취소된 참가자 정보의 상태를 '관리자 취소'로 변경합니다.

        Args:
            applicant_info: ApplicantInfo 객체

        Returns:
            applicant_info: 업데이트된 ApplicantInfo 객체
        """
        participant_info = ParticipantInfo.objects.filter(
            applicant_info=applicant_info).delete()
        applicant_info.change_status_to_admin_canceled()
        if participant_info is None:
            return applicant_info
        self._create_participant_from_waiting_list(applicant_info.competition)

        return applicant_info

    def _create_participant_from_waiting_list(self, competition):
        """
        대기 중인 참가자 중 가장 높은 대기번호를 가진 참가자 정보를 참가자 정보로 생성하는 메서드.

        이 메서드는 다음 작업을 수행합니다:
        1. 대기 중인 참가자 중 가장 높은 대기번호를 가진 참가자 정보를 찾아 참가자 정보를 생성합니다.

        Args:
            competition: Competition 객체
        """
        waiting_participant = ApplicantInfo.objects.filter(
            competition=competition, status='pending_participation').order_by('waiting_number').first()
        if waiting_participant:
            self._create_participant(waiting_participant)

        return None

    def _create_or_update_set(self, match, set_data):
        """
        경기 결과를 입력하거나 수정하는 메서드.

        이 메서드는 다음 작업을 수행합니다:
        1. 기존 세트 정보가 없고 점수가 없는 경우, 아무 작업도 수행하지 않습니다.
        2. 기존 세트 정보가 없고 점수가 있는 경우, 세트 정보를 생성합니다.
        3. 생성되거나 기존 세트 정보에 점수를 입력하거나 수정합니다.

        Args:
            match: Match 객체
            set_data: Set 객체 정보

        Returns:
            set: Set 객체
        """
        set_number = set_data.get('set_number')
        a_score = set_data.get('a_score')
        b_score = set_data.get('b_score')

        result_set = match.set_list.filter(set_number=set_number).first()
        if result_set is None and a_score is None and b_score is None:
            return None

        if result_set is None:
            result_set = match.set_list.create(set_number=set_number)

        result_set.a_score = a_score
        result_set.b_score = b_score
        result_set.save()

        return result_set

    def _create_point(self, match, user, point_entry, tier, match_type):
        """
        경기에 승점을 추가하는 메서드.
        """
        Point.objects.create(
            points=point_entry['points'],
            expired_date=point_entry.get('expired_date'),
            tier=tier,
            match_type=match_type,
            match=match,
            user=user
        )

    def _get_object_or_404(self, model, **kwargs):
        """
        주어진 조건에 맞는 객체를 반환하는 메서드.

        Args:
            model: 모델 클래스
            **kwargs: 필터링 조건

        Returns:
            object: 주어진 조건에 맞는 객체
        """
        return get_object_or_404(model, **kwargs)
