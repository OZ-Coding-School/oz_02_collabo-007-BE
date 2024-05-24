from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from competition.models import Competition

class ApplicantInfo(TimeStampedModel, SoftDeleteModel):
    DEPOSIT_CHOICES = (
        ('un_paid', '입금 전'),
        ('paid', '입금확인'),
        ('canceled', '취소'),
    )
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=15, choices=DEPOSIT_CHOICES, default='un_paid')
    expired_date = models.DateTimeField(null=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='applicants')
    is_waiting = models.BooleanField(default=False)   
    
    
    def __str__(self):
        return f"{self.id} / {self.competition.name}"

    class Meta:
        db_table = 'applicant_info'