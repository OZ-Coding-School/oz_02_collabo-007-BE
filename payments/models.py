from django.db import models
from applicant_info.models import ApplicantInfo
from core.models import TimeStampedModel, SoftDeleteModel


class Payment(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    applicant_info = models.OneToOneField(
        ApplicantInfo, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} / {self.amount}"


class Refund(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, related_name='refund')
    refund_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"Refund for {self.id} / {self.amount}"
