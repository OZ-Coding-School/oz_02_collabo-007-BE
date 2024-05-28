from rest_framework import serializers
from team.models import Team
from custom_admin.club.serializers import ClubListSerializer
from django.contrib.auth import get_user_model


class TeamDetailSerializer(serializers.ModelSerializer):
    club = ClubListSerializer(read_only=True)
    image_file = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)
    description = serializers.CharField(required=False, allow_blank=True)
    delete_image = serializers.BooleanField(write_only=True, required=False)

    def get_image_url(self, obj):
        return obj.image_url.image_url if obj.image_url else None

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'club', 'image_file', 'delete_image',
                  'image_url', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'club')


User = get_user_model()


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'gender')
        read_only_fields = ('id', 'username', 'phone', 'gender')
