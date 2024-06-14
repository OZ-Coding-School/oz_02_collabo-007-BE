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
        user = obj.get('user')
        if user:
            return {
                'id': user.id,
                'username': user.username,
            }
        return None

    def get_club(self, obj):
        user = obj.get('user')
        if user.club:
            return {
                'id': user.club.id,
                'name': user.club.name,
            }
        return None

    def get_tier(self, obj):
        tier = obj.get('tier')
        if tier:
            return {
                'id': tier.id,
                'name': tier.name,
                'match_type_details': {
                    'gender': tier.match_type.gender,
                    'type': tier.match_type.type
                }
            }
        return None
    
    def get_image_url(self, obj):
        user = obj.get('user')
        if user and user.image_url:
            return user.image_url.image_url
        return None
        
            
    
    
    
    
    
    

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
        team = obj['team']
        if team:
            return {
                'id': team.id,
                'name': team.name,
            }
        return None

    def get_club(self, obj):
        team = obj['team']
        if team and team.club:
            return {
                'id': team.club.id,
                'name': team.club.name,
            }
        return None

    def get_image_url(self, obj):
        team = obj['team']
        if team and team.image_url:
            return team.image_url.image_url
        return None