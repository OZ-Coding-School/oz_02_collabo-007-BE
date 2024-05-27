from rest_framework import serializers
from custom_admin.club.serializers import ClubListSerializer
from team.models import Team
from club.models import Club
from image_url.models import ImageUrl
from image_url.utils import S3ImageUploader


class TeamDetailSerializer(serializers.ModelSerializer):
    club = ClubListSerializer(read_only=True)
    image_file = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)
    description = serializers.CharField(required=False, allow_blank=True)
    delete_image = serializers.BooleanField(write_only=True, required=False)

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'club', 'image_file', 'delete_image',
                  'club', 'image_url', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'club')

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image_file', None)
        delete_image = validated_data.get('delete_image', False)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if delete_image and instance.image_url:
            image_url_instance = instance.image_url
            instance.image_url = None
            instance.save()
            image_url_instance.delete()

        if image_data and hasattr(image_data, 'size') and image_data.size > 0:
            self._upload_image(instance, image_data)

        instance.save()
        return instance

    def _upload_image(self, team, image_data):
        uploader = S3ImageUploader()
        file_url, extension, size = uploader.upload_file(image_data)

        image_instance = ImageUrl.objects.create(
            image_url=file_url,
            extension=extension,
            size=size
        )
        team.image_url = image_instance
