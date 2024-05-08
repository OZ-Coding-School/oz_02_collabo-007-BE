from django.db import models
from core.models import TimeStampedModel

class Club(TimeStampedModel):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.ForeignKey('image_url.ImageUrl', on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name


    class Meta:
        db_table = 'club'
