from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from participant_info.models import ParticipantInfo
from users.models import CustomUser


class Participant(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    participant_info = models.ForeignKey(
        ParticipantInfo, on_delete=models.CASCADE, related_name='participants')

    def __str__(self):
        return f"{self.user.username} / {self.participant_info.competition.name} / {self.participant_info.id}"

    class Meta:
        db_table = 'participant'
