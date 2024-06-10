from django.forms import CharField
from rest_framework import serializers

from match.models import Match
from set.models import Set


class SetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['set_number', 'a_score', 'b_score']


class MatchDetailSerializer(serializers.ModelSerializer):
    sets = SetDataSerializer(many=True)
    winner = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Match
        fields = ('id', 'sets',  'winner')
        read_only_fields = ['id']
