from applicant_info.models import ApplicantInfo
from django.db import transaction
from competition.models import Competition
from participant.models import Participant
from participant_info.models import ParticipantInfo
from payments.models import Payment, Refund
from match.models import Match


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
            match = Match.objects.create(**match_data)

        return match

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
