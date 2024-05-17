from django.contrib import admin
from .models import Club

class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone', 'image_url')


admin.site.register(Club, ClubAdmin)