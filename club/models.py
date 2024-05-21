from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from custom_admin.club.manager import ClubManager


class Club(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.ForeignKey(
        'image_url.ImageUrl', on_delete=models.DO_NOTHING, blank=True, null=True)
    objects = models.Manager()
    admin_objects = ClubManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'club'
