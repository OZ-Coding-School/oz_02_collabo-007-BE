from rest_framework import serializers
from .models import Applicant
from users.models import CustomUser
class ApplicantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Applicant
        fields = '__all__'


class CompetitionApplicantSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_phone = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['user_name','user_phone']

    def get_user_name(self, obj):
        return obj.user.username  # Applicant의 user 모델의 name 필드 반환

    def get_user_phone(self, obj):
        return obj.user.phone  # Applicant의 user 모델의 phone 필드 반환
