from rest_framework import serializers
from .models import Applicant
from users.models import CustomUser
class ApplicantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())



    class Meta:
        model = Applicant
        fields = '__all__'