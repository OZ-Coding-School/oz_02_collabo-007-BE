from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers


class AdminLoginSerializer(TokenObtainPairSerializer):
    username_field = 'phone'

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['phone'] = user.phone

        return token

    def validate(self, attrs):
        # 'username' 대신 'phone'을 사용하여 인증
        authenticate_kwargs = {
            'phone': attrs.get(self.username_field),
            'password': attrs.get('password'),
        }

        self.user = authenticate(**authenticate_kwargs)
        if self.user is None or not self.user.is_active:
            raise serializers.ValidationError(
                '로그인에 실패하였습니다. 전화번호와 비밀번호를 확인해 주세요.', code=401)

        if not self.user.is_staff and not self.user.is_superuser:
            raise serializers.ValidationError(
                '어드민 권한이 없습니다.', code=403)

        role = 'coach' if self.user.is_staff else 'admin'

        # 토큰 발급
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        data['user'] = {
            'id': self.user.id,
            'phone': self.user.phone,
            'username': self.user.username,
            'role': role,
            'club_id': self.user.club_id,
            'profile': self.user.image_url.image_url if self.user.image_url else '',
        }

        return data
