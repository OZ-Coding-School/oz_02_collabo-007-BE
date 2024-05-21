from django.contrib import admin
from .models import ImageUrl

class ImageUrlAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_url', 'extension', 'size')


admin.site.register(ImageUrl, ImageUrlAdmin)
