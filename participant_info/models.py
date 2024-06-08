from django.db import models
from applicant_info.models import ApplicantInfo
from core.models import TimeStampedModel, SoftDeleteModel
from competition.models import Competition


class ParticipantInfo(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name='participants')
    applicant_info = models.OneToOneField(
        ApplicantInfo, related_name='participant_info', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f"{self.id} / {self.competition.name}"

    class Meta:
        db_table = 'participant_info'
