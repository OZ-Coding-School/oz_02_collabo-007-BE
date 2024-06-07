from django.contrib import admin
from .models import ParticipantInfo

class ParticipantInfoAdmin(admin.ModelAdmin):
    list_display = ('id','competition')
    ordering = ('-id',)
admin.site.register(ParticipantInfo)