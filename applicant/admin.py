from django.contrib import admin
from .models import Applicant

class ApplicantAdmin(admin.ModelAdmin):
    model = Applicant
    list_display = ('id', 'user', 'applicant_info')  
    ordering = ('-id',) 

admin.site.register(Applicant, ApplicantAdmin)

