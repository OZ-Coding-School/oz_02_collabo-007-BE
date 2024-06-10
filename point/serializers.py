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







# 유저 랭킹 조회 serializer
class UserRankingSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    image_url = serializers.SerializerMethodField()
    user= serializers.SerializerMethodField()
    club = serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()

    class Meta:
        model = Point
        fields = ('match_type_details', 'rank', 'total_points', 'user', 'tier',  'club', 'image_url')

    # 각 필드 이름 가져오는 인스턴스 메서드
    def get_user(self, obj):
        if obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
            }
        return None

    def get_club(self, obj):
        if obj.user.club:
            return {
                'id': obj.user.club.id,
                'name': obj.user.club.name,
            }
        return None

    def get_tier(self, obj):
        if obj.tier:
            return {
                'id': obj.tier.id,
                'name': obj.tier.name,
                'match_type_details': {
                    'gender': obj.tier.match_type.gender,
                    'type': obj.tier.match_type.type
                }
            }
        return None
    
    def get_image_url(self, obj):
        if obj.user.image_url is None:
            return None
        return obj.user.image_url.image_url
    
    
    
    
    
    
    

# 팀 랭킹 조회 serializer
class TeamRankingSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    image_url = serializers.SerializerMethodField()
    team= serializers.SerializerMethodField()
    club = serializers.SerializerMethodField()

    class Meta:
        model = Point
        fields = ('rank', 'total_points', 'team', 'club', 'image_url', 'match_type_details')

    # 각 필드 이름 가져오는 인스턴스 메서드
    def get_team(self, obj):
        if obj.team:
            return {
                'id': obj.team.id,
                'name': obj.team.name,
            }
        return None


    def get_club(self, obj):
        if obj.team.club:
            return {
                'id': obj.team.club.id,
                'name': obj.team.club.name,
            }
        return None
 
    def get_image_url(self, obj):
        if obj.team.image_url is None:
            return None
        return obj.team.image_url.image_url