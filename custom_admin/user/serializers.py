from rest_framework import serializers
from club.models import Club
from django.contrib.auth import get_user_model
from custom_admin.club.serializers import ClubListSerializer
from image_url.models import ImageUrl
from image_url.utils import S3ImageUploader

User = get_user_model()
INITIAL_PASSWORD = '123456'


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

    def get_image_url(self, obj):
        return obj.image_url.image_url if obj.image_url else None

    class Meta:
        model = User
        fields = ('id', 'phone', 'username', 'birth', 'gender',
                  'club', 'club_id', 'image_file', 'image_url', 'created_at', 'updated_at', 'delete_image')
        read_only_fields = ('id', 'created_at', 'updated_at', 'club')

    def create(self, validated_data):
        image_data = validated_data.get('image_file')
        club = validated_data.get('club')

        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=INITIAL_PASSWORD,
            username=validated_data['username'],
            birth=validated_data.get('birth'),
            gender=validated_data.get('gender'),
            club=club
        )

        if image_data and hasattr(image_data, 'size') and image_data.size > 0:
            self._upload_image(user, image_data)

        user.save()
        return user

    def update(self, instance, validated_data):
        print(validated_data)
        print(instance)
        image_data = validated_data.get('image_file')
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

    def _upload_image(self, user, image_data):
        uploader = S3ImageUploader()
        file_url, extension, size = uploader.upload_file(image_data)
        image_instance = ImageUrl.objects.create(
            image_url=file_url,
            extension=extension,
            size=size
        )
        user.image_url = image_instance
