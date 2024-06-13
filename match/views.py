from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MatchSerializer, MatchRecordSerializer
from .models import Match
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.models import CustomUser

# 토너먼트리그 대회현황 조회
class MatchRoundAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('roundnumber', openapi.IN_QUERY, description="Match round number", type=openapi.TYPE_INTEGER),
        ],
        operation_summary='대회현황',
        operation_description='쿼리파라미터를 사용해서 매치 라운드통해 정보를 불러올 수 있습니다.(예시 http://127.0.0.1:8000/api/v1/competitions/1/status/?roundnumber=1)')
    #match_round와 competition_id를 통해 매치 정보 가져오기
    def get(self, request, competition_id):
        roundnumber = request.query_params.get('roundnumber', None)
        filters = {'competition_id': competition_id}
        if roundnumber is not None:
            filters['match_round'] = roundnumber

        matches = Match.objects.filter(**filters) if filters else Match.objects.all()
  
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MatchRecordAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('usersid', openapi.IN_QUERY, description="User ID", type=openapi.TYPE_INTEGER),
        ],
        operation_summary='내 전적 조회',
        operation_description='쿼리파라미터를 사용해서 유저의 매치 전적을 조회합니다.(예시 http://127.0.0.1:8000/api/v1/competitions/record/?user_id=1)'
        )
    def get(self, request):
        user_id = request.query_params.get('user_id', None)
        if user_id is None:
            return Response("존재하지 않는 user_id입니다.", status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response("유효하지 않은 user_id입니다.", status=status.HTTP_404_NOT_FOUND)

        serializer = MatchRecordSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

