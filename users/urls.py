from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .views import(
                    CreateUserView,
                    LoginView,
                    RefreshAccessTokenView,
                    LogoutView,
                    MyProfileView,
                    UserDetailView,
                    UpdateMyProfileAPIView,
                    ChangePasswordView
)


urlpatterns = [
    path('auth/token/refresh/', RefreshAccessTokenView.as_view(), name='token_refresh'), # 토큰 리프레시
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # 토큰 검증 # 리프레시토큰 갱신 api
    path('auth/signup/', CreateUserView.as_view(), name='signup'), # 회원가입 api
    path('auth/signin/', LoginView.as_view(), name='login'), # 로그인 api
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('user/myprofile/', MyProfileView.as_view(), name='my-profile'), # 내 프로필 상세정보 조회
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'), # 특정 유저 상세정보 조회
    path('user/myprofile/update/', UpdateMyProfileAPIView.as_view(), name='update-my-profile'), # 내 프로필 업데이트 api
    path('user/myprofile/update/password/', ChangePasswordView.as_view(), name='change-password'),
]


