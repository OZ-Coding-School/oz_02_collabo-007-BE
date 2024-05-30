from django.contrib import admin
from .models import Point

class PointAdmin(admin.ModelAdmin):
    list_display = (
                    'id',
                    'user',
                    'match_type',
                    'tier',
                    'team',
                    'points',
                    'expired_date',
    )


admin.site.register(Point, PointAdmin)
