from django.db import models
from django.utils import timezone
from core.models import SoftDeleteModel, TimeStampedModel
from users.models import CustomUser
from club.models import Club

class ClubApplicant(SoftDeleteModel, TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING, related_name='applicants')
    date_applied = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=255, choices=(('pending', '대기'), ('approved', '승인'), ('rejected', '거절')), default='pending')

    def __str__(self):
        return f'{self.user.username} - {self.club.name}'
    
    
    class Meta:
        db_table = 'club_applicant'
