from rest_framework.permissions import AllowAny
from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, parsers
from rest_framework_simplejwt.views import TokenObtainPairView
from djangorestframework_camel_case.parser import CamelCaseFormParser, CamelCaseMultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (CreateUserSerializer,
                          PhoneCheckSerializer,
                          CustomTokenObtainPairSerializer,
                          UserInfoSerializer,
                          UpdateMyProfileSerializer,
                          ChangePasswordSerializer,
                          MyProfileRankingSerializer,
                          MyProfileTeamRankingSerializer,
                          MainRankingSerializer,
                          UserRankingSearchSerializer,
                          UserTeamRankingSearchSerializer
                          )

from django.utils import timezone
from django.db.models import Sum
from rest_framework.exceptions import NotFound
from point.models import Point
from django.shortcuts import get_object_or_404
from matchtype.models import MatchType
from django.db.models import Q
from tier.models import Tier
from team.models import Team

User = get_user_model()


# 회원가입 view ##
class CreateUserView(APIView):
    """
    회원가입 API
    """
    parser_classes = (CamelCaseFormParser, CamelCaseMultiPartParser)

    @swagger_auto_schema(
        operation_summary='유저 회원가입',
        operation_description='회원가입 API',
        request_body=CreateUserSerializer,
        responses={
            200: openapi.Response('회원가입이 완료 되었습니다'),
            400: openapi.Response('입력값을 확인해주세요')
        }

    )
    def post(self, request, *args, **kwargs):
        serializer = CreateUserSerializer(
            data=request.data)  # request.data를 직접 사용

        if serializer.is_valid():
            user = serializer.save()
            token = CustomTokenObtainPairSerializer.get_token(
                user)  # 사용자를 위한 토큰 생성
            response = Response({
                'message': '회원가입이 완료 되었습니다',
                'access': str(token.access_token)
            }, status=status.HTTP_201_CREATED)

            # 생성된 리프레시 토큰을 쿠키에 설정
            response.set_cookie('refresh', value=str(token), httponly=True)
            return response

        return Response({
            'code': 400,
            'message': '입력값을 확인해주세요',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PhoneCheckView(APIView):
    """
    휴대폰번호 중복 확인 API
    """
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)

    @swagger_auto_schema(
        operation_summary='휴대폰번호 중복확인',
        operation_description='휴대폰번호 중복 확인 API',
        request_body=PhoneCheckSerializer,
        responses={
            200: openapi.Response('사용 가능한 휴대폰 번호 입니다'),
            400: openapi.Response('사용 불가능한 휴대폰 번호 입니다', PhoneCheckSerializer)
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = PhoneCheckSerializer(data=request.data)

        if serializer.is_valid():
            return Response({
                'message': '사용 가능한 휴대폰 번호 입니다'
            }, status=status.HTTP_200_OK)

        return Response({
            'code': 400,
            'message': '사용 불가능한 휴대폰 번호 입니다',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


## 로그인 ##
class LoginView(TokenObtainPairView):
    """
    유저 로그인 API
    """
    parser_classes = (CamelCaseFormParser, CamelCaseMultiPartParser)

    @swagger_auto_schema(
        operation_summary='유저 로그인',
        operation_description='유저 로그인 API',
        request_body=CustomTokenObtainPairSerializer,
        responses={
            200: openapi.Response('로그인 완료'),
            400: openapi.Response('로그인에 실패하였습니다. 전화번호와 비밀번호를 확인해 주세요')
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        res = super().post(request, *args, **kwargs)

        response = Response({
            "message": "로그인 완료",
            "access": str(res.data.get('access', None))
        }, status=status.HTTP_200_OK)

        response.set_cookie("refresh", res.data.get(
            'refresh', None), httponly=True)

        return response


## 로그아웃 ##
class LogoutView(APIView):
    @swagger_auto_schema(
        operation_summary='유저 로그아웃',
        operation_description='유저 로그아웃 API',
    )
    def post(self, request, *args, **kwargs):
        response = Response({
            'detail': '로그아웃되었습니다'
        }, status=status.HTTP_200_OK)

        response.delete_cookie('refresh')

        return response


## 액세스 토큰 리프레시 ##


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

    parser_classes = (CamelCaseFormParser, CamelCaseMultiPartParser)

    @swagger_auto_schema(
        operation_summary='내 프로필 편집',
        operation_description='내 프로필을 업데이트하는 API',
        request_body=UpdateMyProfileSerializer,
        responses={
            200: openapi.Response(''),
            400: openapi.Response('')
        }
    )
    def put(self, request, format=None):
        user = request.user
        serializer = UpdateMyProfileSerializer(
            user, data=request.data, partial=True)  # 부분 업데이트를 위해 partial=True를 추가
        if serializer.is_valid():
            serializer.save()
            # 업데이트가 성공적으로 완료되면, serializer의 데이터와 함께 200 OK 응답을 반환
            return Response(serializer.data, status=status.HTTP_200_OK)
        # 유효성 검사에 실패한 경우, 오류 메시지와 함께 400 Bad Request 응답을 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 유저 비밀번호 변경 시리얼라이저
class ChangePasswordView(APIView):
    """
    유저 비밀번호 변경 api
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='유저 비밀번호 변경',
        operation_description='유저 비밀번호 변경 API',
        request_body=ChangePasswordSerializer,
        responses={
            200: openapi.Response('비밀번호가 변경되었습니다'),
            400: openapi.Response('기존 비밀번호가 일치하지 않습니다')
        }
    )
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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    특정 유저 상세 정보를 제공하는 API
    """
    @swagger_auto_schema(
        operation_summary='특정 유저 상세 정보 조회',
        operation_description='특정 유저 상세 정보를 제공하는 API',
    )
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': '해당 유저가 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


        
 
class MyProfileView(APIView):
    """
    로그인한 유저 정보를 제공하는 API
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='로그인한 유저 정보를 제공하는 API',
        operation_description='로그인한 자기 자신의 정보를 조회하는 API 입니다.',
        responses={
            200: UserInfoSerializer(many=True),
            401: 'Authentication Error'
        }
    )
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # request.user에는 JWT 토큰을 통해 인증된 사용자의 인스턴스가 포함되어 있습니다.
        user = request.user
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)







# 로그인한 유저 랭킹을 제공하는 API
class MyprofileRankingsView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
    operation_summary='로그인한 유저 랭킹을 조회하는 API',
    operation_description='로그인한 사용자의 단식/복식/팀 랭킹을 조회합니다.',
    responses={
        200: openapi.Response('', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mainRanking': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ranking': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                ),
                'singleRanking': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'userId': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'userName': openapi.Schema(type=openapi.TYPE_STRING),
                            'ranking': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                        }
                    )
                ),
                'doubleRanking': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'userId': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'userName': openapi.Schema(type=openapi.TYPE_STRING),
                            'ranking': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                        }
                    )
                ),
                'teamRanking': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'teamId': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'teamName': openapi.Schema(type=openapi.TYPE_STRING),
                        'ranking': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                    }
                ),
            }
        ))
    }
)

    def get(self, request, *args, **kwargs):
        current_time = timezone.now()
        
        # 로그인된 사용자의 티어 정보를 가져옴
        user_tiers = request.user.tiers.all()
        
        # 사용자가 속한 모든 매치 타입을 가져옴
        user_match_types = [tier.match_type for tier in user_tiers]
        
    

        
        # 매치 타입별 쿼리셋 생성
        single_queryset = Point.objects.filter(
            expired_date__gte=current_time,
            match_type__type='single',
            match_type__in=user_match_types
        ).values('user', 'tier').annotate(total_points=Sum('points')).order_by('-total_points')
        
        double_queryset = Point.objects.filter(
            expired_date__gte=current_time,
            match_type__type='double',
            match_type__in=user_match_types
        ).values('user', 'tier').annotate(total_points=Sum('points')).order_by('-total_points')
        
        team_queryset = Point.objects.filter(
            expired_date__gte=current_time,
            match_type__type='team',
        ).values('team').annotate(total_points=Sum('points')).order_by('-total_points')

        if not single_queryset.exists() and not double_queryset.exists() and not team_queryset.exists():
            return Response({"detail": "랭킹 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 단식 순위를 계산하여 각 객체에 할당
        single_ranked_queryset = []
        for idx, obj in enumerate(single_queryset, start=1):
            user_id = obj['user']
            user = User.objects.get(id=user_id)
            tier_id = obj['tier']
            tier = Tier.objects.get(id=tier_id)
            obj['user'] = user
            obj['tier'] = tier
            obj['rank'] = idx
            single_ranked_queryset.append(obj)

        # 복식 순위를 계산하여 각 객체에 할당
        double_ranked_queryset = []
        for idx, obj in enumerate(double_queryset, start=1):
            user_id = obj['user']
            user = User.objects.get(id=user_id)
            tier_id = obj['tier']
            tier = Tier.objects.get(id=tier_id)
            obj['user'] = user
            obj['tier'] = tier
            obj['rank'] = idx
            double_ranked_queryset.append(obj)

        # 팀 순위를 계산하여 각 객체에 할당
        team_ranked_queryset = []
        for idx, obj in enumerate(team_queryset, start=1):
            team_id = obj['team']
            team = Team.objects.get(id=team_id)
            obj['team'] = team
            obj['rank'] = idx
            team_ranked_queryset.append(obj)

        # 단식 랭킹 정보
        single_ranking = []
        for obj in single_ranked_queryset:
            user = obj['user']
            user_id = user.id
            if user == request.user:
                single_ranking.append(obj)

        # 복식 랭킹 정보
        double_ranking = []
        for obj in double_ranked_queryset:
            user = obj['user']
            user_id = user.id
            if user == request.user:
                double_ranking.append(obj)

        # 팀 랭킹 정보
        team_ranking = next((obj for obj in team_ranked_queryset if obj['team'] == request.user.team), None)
        
        
        
        
        single_ranking_serializer = MyProfileRankingSerializer(single_ranking, many=True, context={"request": request})
        double_ranking_serializer = MyProfileRankingSerializer(double_ranking, many=True, context={"request": request})
        my_team_ranking_serializer = MyProfileTeamRankingSerializer(team_ranking, context={"request": request})

        response_data = {
            'main_ranking': MainRankingSerializer(request.user).data['main_ranking'],
            'single': single_ranking_serializer.data if single_ranking else None,
            'double': double_ranking_serializer.data if double_ranking else None,
            'team': [my_team_ranking_serializer.data] if team_ranking else None
        }

        return Response(response_data, status=status.HTTP_200_OK)
        
        # except NotFound as e:
        #     return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        # except Exception as e:/
        #     return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# 대표 랭킹 설정 API
class SetMainRankingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='대표 랭킹 설정 API',
        operation_description='유저의 대표 랭킹을 설정하는 API',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mainRanking': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['single', 'double', 'team'],
                    description='(\'single\', \'double\', \'team\' 중 하나)'
                )
            }
        ),
        responses={
            200: openapi.Response('메인 랭킹이 업데이트되었습니다.'),
            400: openapi.Response('main_ranking 값은 \'single\', \'double\', \'team\' 중 하나여야 합니다.')
        }
    )
    def post(self, request, *args, **kwargs):
        main_ranking = request.data.get('main_ranking')
        if main_ranking not in ['single', 'double', 'team']:
            return Response({"detail": "main_ranking 값은 'single', 'double', 'team' 중 하나여야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.main_ranking = main_ranking
        request.user.save()

        return Response({"detail": f"메인 랭킹이 '{main_ranking}'으로 업데이트되었습니다."}, status=status.HTTP_200_OK)
    
    
    
    

# 유저별 랭킹 조회 API
class UserRankingSearchView(APIView):
    
    @swagger_auto_schema(
    operation_summary='특정 유저 랭킹을 조회하는 API',
    operation_description='특정 유저의 단식/복식/팀 랭킹을 조회합니다.',
    responses={
        200: openapi.Response('', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'singleRanking': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'userId': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'userName': openapi.Schema(type=openapi.TYPE_STRING),
                            'ranking': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                        }
                    )
                ),
                'doubleRanking': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'userId': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'userName': openapi.Schema(type=openapi.TYPE_STRING),
                            'ranking': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                        }
                    )
                ),
                'teamRanking': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'teamId': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'teamName': openapi.Schema(type=openapi.TYPE_STRING),
                        'ranking': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'score': openapi.Schema(type=openapi.TYPE_NUMBER),
                    }
                ),
            }
        ))
    }
)
    
    def get(self, request, user_id, *args, **kwargs):
        current_time = timezone.now()
        
        user = User.objects.get(id=user_id)
        
        user_tiers = user.tiers.all()
        
        # 사용자가 속한 모든 매치 타입을 가져옴
        user_match_types = [tier.match_type for tier in user_tiers]
        
        # 매치 타입별 쿼리셋 생성
        single_queryset = Point.objects.filter(
            expired_date__gte=current_time,
            match_type__type='single',
            match_type__in=user_match_types,
        ).values('user', 'tier').annotate(total_points=Sum('points')).order_by('-total_points')
        
        double_queryset = Point.objects.filter(
            expired_date__gte=current_time,
            match_type__type='double',
            match_type__in=user_match_types,
        ).values('user', 'tier').annotate(total_points=Sum('points')).order_by('-total_points')
        
        team_queryset = Point.objects.filter(
            expired_date__gte=current_time,
            match_type__type='team',
        ).values('team').annotate(total_points=Sum('points')).order_by('-total_points')

        if not single_queryset.exists() and not double_queryset.exists() and not team_queryset.exists():
            return Response({"detail": "랭킹 정보를 찾을 수 없습니다."}, status=status.HTTP_200_OK)

        # 단식 순위 계산 및 필터링
        single_ranked_queryset = []
        for idx, obj in enumerate(single_queryset, start=1):
            user_obj = User.objects.get(id=obj['user'])
            tier_obj = Tier.objects.get(id=obj['tier'])
            obj['user'] = user_obj
            obj['tier'] = tier_obj
            obj['rank'] = idx
            if user_obj == user:
                single_ranked_queryset.append(obj)
        print(single_ranked_queryset)

        # 복식 순위 계산 및 필터링
        double_ranked_queryset = []
        for idx, obj in enumerate(double_queryset, start=1):
            user_obj = User.objects.get(id=obj['user'])
            tier_obj = Tier.objects.get(id=obj['tier'])
            obj['user'] = user_obj
            obj['tier'] = tier_obj
            obj['rank'] = idx
            if user_obj == user:
                double_ranked_queryset.append(obj)

        # 팀 순위 계산 및 필터링
        team_ranked_queryset = []
        for idx, obj in enumerate(team_queryset, start=1):
            team_obj = Team.objects.get(id=obj['team'])
            obj['team'] = team_obj
            obj['rank'] = idx
            if team_obj == user.team:
                team_ranked_queryset.append(obj)
        print(team_ranked_queryset)   
        

        # Serializer 선언
        single_ranking_serializer = UserRankingSearchSerializer(single_ranked_queryset, many=True, context={"request": request})
        double_ranking_serializer = UserRankingSearchSerializer(double_ranked_queryset, many=True, context={"request": request})
        my_team_ranking_serializer = UserTeamRankingSearchSerializer(team_ranked_queryset, many=True, context={"request": request})

        # 응답 데이터 구성
        response_data = {
            'single': single_ranking_serializer.data if single_ranked_queryset else None,
            'double': double_ranking_serializer.data if double_ranked_queryset else None,
            'team': my_team_ranking_serializer.data if team_ranked_queryset else None
        }

        return Response(response_data, status=status.HTTP_200_OK)