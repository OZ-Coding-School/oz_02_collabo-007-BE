from django.contrib import admin
from .models import Competition



class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'status', 'total_rounds', 'total_sets', 'code', 'match_type', 'tier', 'max_participants')

admin.site.register(Competition, CompetitionAdmin)