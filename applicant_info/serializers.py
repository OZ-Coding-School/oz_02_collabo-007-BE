from rest_framework import serializers
from .models import ApplicantInfo
from applicant.serializers import ApplicantSerializer
class ApplicantInfoSerializer(serializers.ModelSerializer):
    applicants = ApplicantSerializer(many=True, read_only=True)
    


    class Meta:
        model = ApplicantInfo
        fields = ['id', 'competition','expired_date', 'applicants', 'waiting_number']


class CompetitionApplicantInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicantInfo
        fields = ['expired_date','waiting_number']