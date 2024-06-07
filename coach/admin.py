from django.contrib import admin
from .models import Coach

class CoachAdmin(admin.ModelAdmin):
    list_display = ('id','club','user')
    ordering = ('-id',)

admin.site.register(Coach,CoachAdmin)
