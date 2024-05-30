from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
from rest_framework import serializers
from matchtype.models import MatchType
from .models import Point
from matchtype.serializers import MatchTypeSerializer


# 승점 부여 serializer
class GivePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'

    def create(self, validated_data):
        # 임시로 승점 유효기간을 1년으로 잡음
        validated_data['expired_date'] = datetime.now() + timedelta(days=365)
        return super().create(validated_data)




class MatchTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchType
        fields = ['gender', 'type']





# 실시간 랭킹 조회 serializer
class LiveRankingSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(read_only=True)
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    image_url = serializers.SerializerMethodField()
    user= serializers.SerializerMethodField()
    club = serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()

    class Meta:
        model = Point
        fields = ('user', 'tier', 'total_points', 'club', 'image_url', 'match_type_details')

    # 각 필드 이름 가져오는 인스턴스 메서드
    def get_user(self, obj):
        if obj.user:
            return obj.user.username
        return None

    def get_club(self, obj):
        if obj.user.club:
            return obj.user.club.name
        return None

    def get_tier(self, obj):
        if obj.tier is None:
            return None
        return obj.tier.name
    
    def get_image_url(self, obj):
        if obj.user.image_url is None:
            return None
        return obj.user.image_url.image_url