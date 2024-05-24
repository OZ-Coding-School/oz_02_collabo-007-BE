from django.db import models
from club.models import Club
from users.models import CustomUser
from core.models import TimeStampedModel, SoftDeleteModel

class Coach(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    club = models.ForeignKey(Club, models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, models.DO_NOTHING)

    def __int__(self):
        return self.id

    class Meta:
        db_table = 'coach'