from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tier
from .serializers import TierSerializer


## 전체 티어 조회
class TierListView(APIView):
    """
    전체 티어 조회
    """
    
    def get(self, request, *args, **kwargs):
        tiers = Tier.objects.all()
        serializer = TierSerializer(tiers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)