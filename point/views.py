from django.utils import timezone
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .models import Point
from rest_framework.response import Response
from .serializers import LiveRankingSerializer



class LiveRankingView(APIView):
    @swagger_auto_schema(
        operation_summary='실시간 매치타입별 랭킹 조회',
        operation_description='실시간 매치타입별 랭킹을 조회가능 (쿼리파라미터 활용해주세요)',
        responses={
            200: LiveRankingSerializer(many=True),
            401: 'Authentication Error',
            403: 'Permission Denied',
            404: 'Not Found'
        }
    )
    def get(self, request, *args, **kwargs):
        current_time = timezone.now()
        # 기본 필터: timezone now 기준 만료되지 않은 승점을 수집
        queryset = Point.objects.filter(expired_date__gte=current_time) 
        # 쿼리 파라미터
        match_type = request.query_params.get('match_type')
        
        if match_type:
            queryset = queryset.filter(match_type__type=match_type)

        # 각 유저의 총 포인트 합산 및 내림차순 정렬 / annotate : 쿼리셋에 집계 값을 추가할 때 사용)
        queryset = queryset.annotate(total_points=Sum('points')).order_by('-total_points')

        serializer = LiveRankingSerializer(queryset, many=True)
        return Response(serializer.data)