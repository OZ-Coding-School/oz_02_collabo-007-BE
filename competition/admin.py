from django.contrib import admin
from .models import Competition, CompetitionResult, CompetitionTeamMatch



class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'status', 'total_rounds', 'total_sets', 'code', 'match_type', 'tier', 'max_participants')

admin.site.register(Competition, CompetitionAdmin)

class CompetitionResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'competition', 'winner', 'runner_up')

# CompetitionResult 모델 등록
admin.site.register(CompetitionResult, CompetitionResultAdmin)


class CompetitionTeamMatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'competition', 'match_type', 'tier', 'game_number']
    search_fields = ['competition__name', 'match_type__name', 'tier__name']
    list_filter = ['competition', 'match_type', 'tier']

admin.site.register(CompetitionTeamMatch, CompetitionTeamMatchAdmin)