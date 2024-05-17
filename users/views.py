from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (CreateUserSerializer,
                          CustomTokenObtainPairSerializer,
                          UserInfoSerializer,
                          UpdateMyProfileSerializer,
                          ChangePasswordSerializer,
) 



User = get_user_model()


# 회원가입 view ##
class CreateUserView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(data=request.data)  # request.data를 직접 사용
        
        if serializer.is_valid():
            user = serializer.save()
            token = CustomTokenObtainPairSerializer.get_token(user)  # 사용자를 위한 토큰 생성
            response = Response({
                'message': '회원가입이 완료 되었습니다',
                'access': str(token.access_token)
            }, status=status.HTTP_201_CREATED)
            
            # 생성된 리프레시 토큰을 쿠키에 설정
            response.set_cookie('refresh',value=str(token), httponly= True)
            return response

        return Response({
            'code': 400,
            'message': '입력값을 확인해주세요',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



## 로그인 ##
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


class LoginView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        res = super().post(request, *args, **kwargs)
        
        response = Response({
            "message": "로그인 완료",
            "access": str(res.data.get('access', None))
            }, status= status.HTTP_200_OK)
        
        response.set_cookie("refresh", res.data.get('refresh', None), httponly= True)
        
        return response
    
    
     
    
## 로그아웃 ##
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({
            'detail': '로그아웃되었습니다'
            }, status=status.HTTP_200_OK)
        
        response.delete_cookie('refresh')
        
        return response



## 액세스 토큰 리프레시 ##
from rest_framework.permissions import AllowAny

class RefreshAccessTokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token is None:
            return Response({"error": "리프레시 토큰이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)

            # 필요하다면 새 리프레시 토큰도 생성하여 반환할 수 있습니다. 
            # new_refresh_token = str(token)

            response = Response()
            response.data = {
                'access': new_access_token,
                # 'refresh': new_refresh_token,
            }

            return response
        except Exception as e:
            return Response({"error": "인증되지 않은 리프레시 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
            

class UpdateMyProfileAPIView(APIView):
    """
     내 프로필을 업데이트하는 API
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user  # Use the currently authenticated user's information.
        serializer = UpdateMyProfileSerializer(user, data=request.data, partial=True)  # 부분 업데이트를 위해 partial=True를 추가합니다.
        if serializer.is_valid():
            serializer.save()
            # 업데이트가 성공적으로 완료되면, serializer의 데이터와 함께 200 OK 응답을 반환합니다.
            return Response(serializer.data, status=status.HTTP_200_OK)
        # 유효성 검사에 실패한 경우, 오류 메시지와 함께 400 Bad Request 응답을 반환합니다.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# 유저 비밀번호 변경 시리얼라이저
class ChangePasswordView(APIView):
    """
    유저 비밀번호 변경 api
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
     
        if serializer.is_valid():
            # 기존 비밀번호
            if not user.check_password(serializer.validated_data['prev_password']):
                return Response({'prev_password': ['기존 비밀번호가 일치하지 않습니다.']}, status=status.HTTP_400_BAD_REQUEST)
            
            # 새로운 비밀번호
            user.set_password(serializer.validated_data['changed_password'])
            user.save()
            return Response({'message': '비밀번호가 변경되었습니다.'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        
        
class UserDetailView(APIView):
    """
    유저 상세 정보를 제공하는 API
    """

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': '해당 유저가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)      
        



class MyProfileView(APIView):
    """
    내 프로필 정보를 제공하는 API
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # request.user에는 JWT 토큰을 통해 인증된 사용자의 인스턴스가 포함되어 있습니다.
        user = request.user
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)