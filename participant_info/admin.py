from django.contrib import admin
from .models import ParticipantInfo
from participant.models import Participant

class ParticipantInfoAdmin(admin.ModelAdmin):
    list_display = ('id','competition','participant_name','second_participant_name')
    ordering = ('-id',)

    # applicant_info를 fk로 갖는 applicant 데이터를 필드로 가져오기
    # 신청자가 여러명인 경우

    def participant_name(self, obj):
        participant = Participant.objects.filter(participant_info=obj).first()
        if participant:
            return participant.user.username

    participant_name.short_description = 'participant name'

    def second_participant_name(self, obj):
        participants = Participant.objects.filter(participant_info=obj)

        if participants.count() == 2:
            participant = participants[1]
            return participant.user.username
            
    second_participant_name.short_description = 'partner name'
admin.site.register(ParticipantInfo, ParticipantInfoAdmin)