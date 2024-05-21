from rest_framework import serializers

from club.models import Club
from image_url.models import ImageUrl
from image_url.utils import S3ImageUploader
from team.models import Team


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

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    class Meta:
        model = Club
        fields = ('id', 'name', 'description', 'address', 'phone', 'description', 'image_file',
                  'image_url', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        image_data = validated_data.pop('image_file', None)
        club = Club.objects.create(
            name=validated_data['name'],
            address=validated_data['address'],
            phone=validated_data['phone'],
            description=validated_data['description']
        )

        if image_data and hasattr(image_data, 'size') and image_data.size > 0:
            uploader = S3ImageUploader()
            file_url, extension, size = uploader.upload_file(image_data)

            image_instance = ImageUrl.objects.create(
                image_url=file_url,
                extension=extension,
                size=size
            )
            club.image_url = image_instance
        club.save()

        return club


class TeamSerializer(serializers.ModelSerializer):
    image_file = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)
    description = serializers.CharField(required=False, allow_blank=True)
    users_count = serializers.SerializerMethodField(read_only=True)

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    def get_users_count(self, obj):
        return obj.users.count()

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'club', 'image_file', 'users_count',
                  'image_url', 'created_at', 'updated_at')
        read_only_fields = ('id', 'users_count', 'created_at', 'updated_at')

    def create(self, validated_data):
        image_data = validated_data.pop('image_file', None)
        team = Team.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            club=validated_data['club']
        )

        if image_data and hasattr(image_data, 'size') and image_data.size > 0:
            uploader = S3ImageUploader()
            file_url, extension, size = uploader.upload_file(image_data)

            image_instance = ImageUrl.objects.create(
                image_url=file_url,
                extension=extension,
                size=size
            )
            team.image_url = image_instance
        team.save()

        return team
