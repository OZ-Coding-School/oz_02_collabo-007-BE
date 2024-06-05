from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from participant_info.models import ParticipantInfo
from users.models import CustomUser

class Participant(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    participant_info = models.ForeignKey(ParticipantInfo, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"유저:{self.user.username} / 신청한 대회:{self.participant_info.competition.name} / 신청정보:{self.participant_info.id}"    
    
    
    class Meta:
        db_table = 'participant'