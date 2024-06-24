from rest_framework import serializers
from club.models import Club
from django.contrib.auth import get_user_model
from custom_admin.club.serializers import ClubListSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    club = ClubListSerializer(read_only=True)
    club_id = serializers.PrimaryKeyRelatedField(
        queryset=Club.objects.all(),
        write_only=True,
        source='club',
        required=False
    )
    image_file = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)
    delete_image = serializers.BooleanField(
        write_only=True, required=False, default=False)
    role = serializers.SerializerMethodField(read_only=True)

    def get_image_url(self, obj):
        return obj.image_url.image_url if obj.image_url else None

    def get_role(self, obj):
        if obj.is_superuser:
            return 'admin'
        elif obj.is_staff:
            return 'coach'
        else:
            return 'user'

    class Meta:
        model = User
        fields = ('id', 'phone', 'username', 'birth', 'gender', 'role',
                  'club', 'club_id', 'image_file', 'image_url', 'created_at', 'updated_at', 'delete_image')
        read_only_fields = ('id', 'created_at', 'updated_at', 'club')
