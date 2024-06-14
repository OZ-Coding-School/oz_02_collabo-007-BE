from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel


class Payment(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    applicant_info = models.OneToOneField(
        'applicant_info.ApplicantInfo',
        on_delete=models.CASCADE,
        related_name='payment',
        null=True,
        blank=True
    )
    team_applicant_info = models.ForeignKey(
        'applicant_info.TeamApplicantInfo',
        on_delete=models.CASCADE,
        related_name='payment',
        null=True,
        blank=True
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} / {self.amount}"

    class Meta:
        db_table = 'payment'


class Refund(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, related_name='refund')
    refund_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Refund for {self.id} / {self.amount}"

    class Meta:
        db_table = 'refund'
