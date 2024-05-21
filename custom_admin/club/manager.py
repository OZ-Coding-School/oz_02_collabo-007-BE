from django.db import models


class ClubManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
