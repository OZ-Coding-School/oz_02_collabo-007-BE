from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from competition.models import Competition

class ApplicantInfo(TimeStampedModel, SoftDeleteModel):
    DEPOSIT_CHOICES = (
        ('unpaid', '입금 대기'),
        ('pending_participation', '참가 대기중'),
        ('confirmed_participation', '참가 완료'),
        ('user_canceled', '사용자 취소'),
        ('admin_canceled', '관리자 취소'),
    )
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, choices=DEPOSIT_CHOICES, default='unpaid')
    expired_date = models.DateTimeField(null=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='applicants')
    waiting_number = models.IntegerField(blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.id} / {self.competition.name}"

    class Meta:
        db_table = 'applicant_info'