from django.db import models
from core.models import TimeStampedModel

class MatchType(TimeStampedModel):
    GENDER_CHOICES = (
        ('male', '남자'),
        ('female', '여자'),
        ('mix', '혼성'),
        ('team','팀'),
    )
    
    TYPE_CHOICES = (
        ('single', '단식'),
        ('duo', '복식'),
        ('team', '팀')
    )
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True)
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, null=True)
    
    
    def __str__(self):
        return f"{self.gender}/{self.type}"       
    class Meta:
        db_table = 'match_type'