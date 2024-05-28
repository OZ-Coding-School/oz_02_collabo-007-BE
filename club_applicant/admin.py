from django.contrib import admin
from .models import ClubApplicant


class ClubApplicantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'club', 'date_applied', 'status')

admin.site.register(ClubApplicant, ClubApplicantAdmin)
