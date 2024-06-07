from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MatchSerializer
from match.models import Match
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# 토너먼트리그 대회현황 조회
class MatchRoundAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('round_number', openapi.IN_QUERY, description="Match round number", type=openapi.TYPE_INTEGER),
        ],
        operation_summary='대회현황',
        operation_description='쿼리파라미터를 사용해서 매치 라운드통해 정보를 불러올 수 있습니다.(예시 /api/v1/status/match/round/?round_number=1)')
    #match_round와 competition_id를 통해 매치 정보 가져오기
    def get(self, request):
        round_number = request.query_params.get('round_number', None)
        filters = {}
        if round_number is not None:
            filters['matchround'] = round_number

        matches = Match.objects.filter(**filters) if filters else Match.objects.all()
  
        serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



