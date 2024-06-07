from django.db import models
from match.models import Match
from core.models import TimeStampedModel

class Set(models.Model):
    id = models.AutoField(primary_key=True)
    setnumber = models.IntegerField(db_column='setNumber', blank=True, null=True)  # Field name made lowercase.
    scorea = models.IntegerField(db_column='scoreA', blank=True, null=True)  # Field name made lowercase.
    scoreb = models.IntegerField(db_column='scoreB', blank=True, null=True)  # Field name made lowercase.
    match_list = models.ForeignKey(Match, models.DO_NOTHING, default=1)

    class Meta:
        db_table = 'set'