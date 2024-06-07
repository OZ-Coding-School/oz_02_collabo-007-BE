from django.db import models
from match.models import Match
from core.models import TimeStampedModel

class Set(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    set_number = models.IntegerField(db_column='setNumber', blank=True, null=True)  # Field name made lowercase.
    a_score = models.IntegerField(db_column='Ascore', blank=True, null=True)  # Field name made lowercase.
    b_score = models.IntegerField(db_column='Bscore', blank=True, null=True)  # Field name made lowercase.
    match_list = models.ForeignKey(Match, models.DO_NOTHING, default=1)

    class Meta:
        db_table = 'set'