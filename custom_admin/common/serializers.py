from rest_framework import serializers
from matchtype.models import MatchType
from tier.models import Tier


class AdminMatchTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchType
        fields = ('id', 'gender', 'type')
        read_only_fields = ('id', 'gender', 'type')


class AdminTierSerializer(serializers.ModelSerializer):
    match_type = AdminMatchTypeSerializer(read_only=True)

    class Meta:
        model = Tier
        fields = ('id', 'name', 'match_type')
        read_only_fields = ('id', 'name', 'match_type')
