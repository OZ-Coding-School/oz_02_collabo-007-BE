from rest_framework import serializers
from .models import Club
from users.models import CustomUser
from coach.models import Coach
from team.models import Team






# 전체 클럽 목록 조회 serializer
class ClubListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ['id', 'name', 'address', 'image_url']

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None


# ***********************클럽 상세정보 serializer ***********************

class ClubDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Club
        fields = ['id', 'address', 'phone', 'name', 'description', 'image_url']

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None


class UserWithTeamInfoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'image_url', 'team')

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    def get_team(self, obj):
        if obj.team:
            return {
                'id': obj.team.id,
                'name': obj.team.name
            }
        return None


class CoachSerializer(serializers.ModelSerializer):
    club = serializers.PrimaryKeyRelatedField(read_only=True)
    user = UserWithTeamInfoSerializer(read_only=True)

    class Meta:
        model = Coach
        fields = ('id', 'user', 'club')


class TeamSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id', 'name', 'image_url')

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None


# ****************************************************************

