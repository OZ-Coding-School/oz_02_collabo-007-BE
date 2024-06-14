from rest_framework import serializers
from .models import Tier
from matchtype.serializers import MatchTypeSerializer


class TierSerializer(serializers.ModelSerializer):
    match_type_details = MatchTypeSerializer(source='match_type',   read_only=True)
    
    class Meta:
        model = Tier
        fields = ['id', 'name', 'match_type_details']