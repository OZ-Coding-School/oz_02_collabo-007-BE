from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from custom_admin.auth.serializers import AdminLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView


class AdminLoginView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary='유저 로그인',
        operation_description='유저 로그인 API',
        request_body=AdminLoginSerializer,
        responses={
            200: '로그인 완료',
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Permission Denied',
            404: 'Not Found',
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            self.serializer_class = AdminLoginSerializer
            res = super().post(request, *args, **kwargs)

            response = Response({
                "message": "로그인 완료",
                "access": str(res.data.get('access', None)),
                "refresh": str(res.data.get('refresh', None)),
                "user": res.data.get('user', None)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            for key, value in e.detail.items():
                if hasattr(value[0], 'code') and value[0].code == 403:
                    response = Response({
                        "message": "관리자 권한이 없습니다."
                    }, status=status.HTTP_403_FORBIDDEN)
                    break
                if hasattr(value[0], 'code') and value[0].code == 401:
                    response = Response({
                        "message": "로그인에 실패하였습니다. 전화번호와 비밀번호를 확인해 주세요."
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    break
                response = Response({
                    "message": value[0]
                }, status=status.HTTP_400_BAD_REQUEST)
                break

        return response


class AdminRefreshView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_summary='토큰 갱신',
        operation_description='토큰 갱신 API',
        responses={
            200: '토큰 갱신 완료',
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Permission Denied',
            404: 'Not Found',
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        try:
            token = RefreshToken(request.data.get('refresh'))
            new_access_token = str(token.access_token)

            response = Response()
            response.data = {
                'access': new_access_token,
            }

            return response
        except Exception as e:
            return Response({"error": "인증되지 않은 리프레시 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)


class AdminMyInfoView(APIView):
    @swagger_auto_schema(
        operation_summary='내 정보 조회',
        operation_description='내 정보 조회 API',
        responses={
            200: '내 정보 조회 완료',
            400: 'Bad Request',
            401: 'Unauthorized',
            403: 'Permission Denied',
            404: 'Not Found',
        }
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        try:
            user = request.user
            if not user:
                raise Exception("로그인이 필요합니다.")
            if not user.is_staff and not user.is_superuser:
                raise Exception("어드민 권한이 없습니다.")
            response = Response({
                "id": user.id,
                "phone": user.phone,
                "username": user.username,
                "role": 'coach' if user.is_staff else 'admin',
                "club_id": user.club_id,
                "profile": user.image_url.image_url if user.image_url else '',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            response = Response({"message": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

        return response
