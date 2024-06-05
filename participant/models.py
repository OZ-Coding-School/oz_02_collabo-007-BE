from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from applicant_info.models import ApplicantInfo
from users.models import CustomUser

class Participant(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    applicant_info = models.ForeignKey(ApplicantInfo, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"유저:{self.user.username} / 신청한 대회:{self.applicant_info.competition.name} / 신청정보:{self.applicant_info.id}"    
    
    
    class Meta:
        db_table = 'participant'