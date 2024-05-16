from rest_framework import serializers

from club.models import Club
from django.contrib.auth import get_user_model

from image_url.models import ImageUrl
from image_url.utils import S3ImageUploader

User = get_user_model()
INITIAL_PASSWORD = '123456'


class UserSerializer(serializers.ModelSerializer):
    club = serializers.PrimaryKeyRelatedField(
        queryset=Club.objects.all(), required=False)
    image_file = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    class Meta:
        model = User
        fields = ('id', 'phone', 'username', 'birth', 'gender',
                  'club', 'image_file', 'image_url', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        image_data = validated_data.pop('image_file', None)
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=INITIAL_PASSWORD,
            username=validated_data['username'],
            birth=validated_data.get('birth'),
            gender=validated_data.get('gender'),
            club=validated_data.get('club', None)
        )

        # image_data가 None이 아니고, 파일 크기가 0보다 큰 경우에만 이미지 업로드 실행
        if image_data and hasattr(image_data, 'size') and image_data.size > 0:
            uploader = S3ImageUploader()
            file_url, extension, size = uploader.upload_file(image_data)

            # 업로드된 이미지 정보를 ImageUrl 인스턴스로 저장
            image_instance = ImageUrl.objects.create(
                image_url=file_url,
                extension=extension,
                size=size
            )
            user.image_url = image_instance  # 사용자 인스턴스에 이미지 인스턴스 할당
        user.save()  # 변경 사항 저장

        return user  # zz
