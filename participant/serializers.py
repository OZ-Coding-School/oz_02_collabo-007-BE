from rest_framework import serializers
from .models import Participant

class ParticipantSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    club_name = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = ['username', 'image_url', 'club_name']

    def get_username(self, obj):
        return obj.user.username if obj.user.username else None

    def get_image_url(self, obj):
        return obj.user.image_url.image_url if obj.user.image_url else None

    def get_club_name(self, obj):
        return obj.user.club.name if obj.user.club else None