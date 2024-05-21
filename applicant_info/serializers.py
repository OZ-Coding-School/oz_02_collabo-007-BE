from rest_framework import serializers
from .models import ApplicantInfo
from applicant.serializers import ApplicantSerializer
class ApplicantInfoSerializer(serializers.ModelSerializer):
    applicants = ApplicantSerializer(many=True, read_only=True)
    


    class Meta:
        model = ApplicantInfo
        fields = ['id', 'competition','expired_date', 'applicants', 'is_waiting']