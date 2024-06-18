from django.contrib import admin
from .models import Match, TeamMatch
from participant.models import Participant
class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'competition', 'winner_id', 'a_team', 'b_team')
    ordering = ('-created_at',)


admin.site.register(Match, MatchAdmin)


class TeamMatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'competition', 'a_team', 'b_team', 'winner_id']
    search_fields = ['competition__name', 'a_team__team__name', 'b_team__team__name']
    list_filter = ['competition', 'a_team__team', 'b_team__team', 'winner_id__team']

admin.site.register(TeamMatch, TeamMatchAdmin)