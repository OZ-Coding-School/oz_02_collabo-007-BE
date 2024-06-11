from rest_framework import serializers
from django.contrib.auth import get_user_model
from club.models import Club
from club_applicant.models import ClubApplicant
from custom_admin.common.serializers import AdminTierSerializer
from team.models import Team
from tier.models import Tier


class ClubListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('id', 'name', 'address', 'phone', 'created_at',
                  'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class ClubSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)
    address = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    delete_image = serializers.BooleanField(
        write_only=True, required=False, default=False)

    def get_image_url(self, obj):
        return obj.image_url.image_url if obj.image_url else None

    class Meta:
        model = Club
        fields = ('id', 'name', 'description', 'address', 'phone', 'description', 'image_file',
                  'image_url', 'created_at', 'updated_at', 'delete_image')
        read_only_fields = ('id', 'created_at', 'updated_at')


class TeamSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)
    description = serializers.CharField(required=False, allow_blank=True)
    users_count = serializers.IntegerField(read_only=True)

    def get_image_url(self, obj):
        return obj.image_url.image_url if obj.image_url else None

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'club', 'image_file', 'users_count',
                  'image_url', 'created_at', 'updated_at')
        read_only_fields = ('id', 'users_count', 'created_at', 'updated_at')


User = get_user_model()


class MemberSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), write_only=True, source='team', required=False)
    tiers = AdminTierSerializer(many=True, read_only=True)
    tiers_id = serializers.PrimaryKeyRelatedField(
        queryset=Tier.objects.all(), write_only=True, source='tiers', required=False, many=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'username', 'team',
                  'team_id', 'tiers', 'tiers_id')
        read_only_fields = ('id', 'phone', 'username', 'team', 'tiers')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tiers_representation = {}

        for tier in representation['tiers']:
            try:
                match_type = tier.get('match_type', {}).get('type')
                if match_type:
                    tiers_representation[match_type] = {
                        'id': tier['id'],
                        'name': tier['name']
                    }
            except KeyError:
                continue
            except TypeError:
                continue

        representation['tiers'] = tiers_representation
        return representation


class ApplicationSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)
    club = ClubListSerializer(read_only=True)

    class Meta:
        model = ClubApplicant
        fields = ('id', 'user', 'club', 'date_applied', 'status')
        read_only_fields = ('id', 'user', 'date_applied', 'club')
