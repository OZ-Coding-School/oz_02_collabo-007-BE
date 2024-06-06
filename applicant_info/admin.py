from django.contrib import admin
from .models import ApplicantInfo
from applicant.models import Applicant


class ApplicantInfoAdmin(admin.ModelAdmin):
    list_display = ('id','status','expired_date','competition_id','competition','applicant_name','second_applicant_name','waiting_number')
    ordering = ('-id',)

    # applicant_info를 fk로 갖는 applicant 데이터를 필드로 가져오기
    # 신청자가 여러명인 경우

    def applicant_name(self, obj):
        applicant = Applicant.objects.filter(applicant_info=obj).first()
        return applicant.user.username

    applicant_name.short_description = 'applicant name'

    def second_applicant_name(self, obj):
        applicants = Applicant.objects.filter(applicant_info=obj)

        if applicants.count() == 2:
            applicant = applicants[1]
            return applicant.user.username
            
    second_applicant_name.short_description = 'partner name'
        
    
    

    
    
admin.site.register(ApplicantInfo, ApplicantInfoAdmin)