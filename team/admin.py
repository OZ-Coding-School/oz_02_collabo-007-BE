from django.contrib import admin
from .models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'club', 'image_url')


admin.site.register(Team, TeamAdmin)

