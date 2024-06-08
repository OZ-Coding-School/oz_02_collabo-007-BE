from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from competition.models import Competition
from users.models import CustomUser


class ApplicantInfo(TimeStampedModel, SoftDeleteModel):
    DEPOSIT_CHOICES = (
        ('unpaid', '입금 대기'),
        ('pending_participation', '참가 대기중'),
        ('confirmed_participation', '참가 완료'),
        ('user_canceled', '사용자 취소'),
        ('admin_canceled', '관리자 취소'),
    )
    id = models.AutoField(primary_key=True)
    status = models.CharField(
        max_length=50, choices=DEPOSIT_CHOICES, default='unpaid')
    expired_date = models.DateTimeField(null=True)
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name='applicants')
    waiting_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} / {self.competition.name}"

    class Meta:
        db_table = 'applicant_info'

    def is_pending(self):
        """
        참가자가 대기 중인지 확인합니다.

        Returns:
            bool: 참가자가 대기 중이면 True, 그렇지 않으면 False
        """
        return self.status == 'pending_participation'

    def is_confirmed(self):
        """
        참가자가 참가 신청이 승인되었는지 확인합니다.

        Returns:
            bool: 참가 신청이 승인되었으면 True, 그렇지 않으면 False
        """
        return self.status == 'confirmed_participation'

    def is_canceled(self):
        """
        참가자가 취소되었는지 확인합니다.

        Returns:
            bool: 참가자가 취소되었으면 True, 그렇지 않으면 False
        """
        return self.status == 'user_canceled' or self.status == 'admin_canceled'

    def change_status_to_confirmed(self):
        """
        참가자의 상태를 '참가 완료'로 변경합니다.
        """
        self.status = 'confirmed_participation'
        self.save()

    def change_status_to_pending(self):
        """
        참가자의 상태를 '참가 대기중'으로 변경합니다.
        """
        self.status = 'pending_participation'
        self.save()

    def change_status_to_admin_canceled(self):
        """
        참가자의 상태를 '관리자 취소'로 변경합니다.
        """
        self.status = 'admin_canceled'
        self.save()

    def get_users(self):
        """
        해당 ApplicantInfo에 연결된 모든 사용자(User)를 반환합니다.

        Returns:
            QuerySet: 연결된 CustomUser 객체들의 QuerySet.
        """
        return CustomUser.objects.filter(applicant__applicant_info=self)
