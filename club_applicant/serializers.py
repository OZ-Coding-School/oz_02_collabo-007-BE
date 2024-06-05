from rest_framework import serializers
from .models import ClubApplicant



# 클럽 신청자 시리얼라이저 (로그인한 유저 정보 조회 API에 활용)
class ClubApplicantSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='club.id')
    name = serializers.ReadOnlyField(source='club.name')

    class Meta:
        model = ClubApplicant
        fields = ['id', 'name', 'status', 'date_applied']