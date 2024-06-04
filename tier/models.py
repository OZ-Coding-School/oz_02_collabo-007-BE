from django.db import models
from matchtype.models import MatchType
from core.models import TimeStampedModel, SoftDeleteModel
class Tier(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    match_type = models.ForeignKey(MatchType, models.DO_NOTHING)
    
    def __str__(self):
        return f'{self.name} ({self.match_type})'

    class Meta:
        db_table = 'tier'