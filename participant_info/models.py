from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from competition.models import Competition

class ParticipantInfo(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    registered_date = models.DateTimeField(null=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE) 
    
    
    def __str__(self):
        return f"{self.id} / {self.competition.name}"

    class Meta:
        db_table = 'participant_info'