from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Tier
from .serializers import TierSerializer


## 전체 티어 조회
class TierListView(APIView):
    """
    전체 티어 조회
    """
    @swagger_auto_schema(
        operation_summary='모든 티어 조회',
        operation_description='모든 티어를 조회합니다.',
        responses={
            200: TierSerializer,
        }
    )
    
    def get(self, request, *args, **kwargs):
        tiers = Tier.objects.all()
        serializer = TierSerializer(tiers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)