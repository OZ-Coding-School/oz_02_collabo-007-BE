from django.contrib import admin
from .models import Match
from participant.models import Participant
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'competition', 'winner_id', 'a_team', 'b_team')
    ordering = ('-created_at',)


admin.site.register(Match, MatchAdmin)

