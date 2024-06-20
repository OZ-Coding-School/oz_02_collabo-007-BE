from django.forms import CharField
from rest_framework import serializers

from match.models import Match, TeamMatch
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
        fields = ('id', 'sets',  'winner', 'team_match_game_number')
        read_only_fields = ['id']
        extra_kwargs = {
            'team_match_game_number': {'required': False}
        }


class TeamMatchDetailSerializer(serializers.ModelSerializer):
    winner = serializers.CharField(required=False, allow_blank=True)
    matches = MatchDetailSerializer(many=True)

    class Meta:
        model = TeamMatch
        fields = ('id', 'matches', 'winner')
        read_only_fields = ['id']


class PointEntrySerializer(serializers.Serializer):
    points = serializers.IntegerField(required=True)
    expired_date = serializers.DateTimeField(required=True)
    user_id = serializers.IntegerField(required=True)
    tier_id = serializers.IntegerField(required=True)
    match_type_id = serializers.IntegerField(required=True)


class AddPointsSerializer(serializers.Serializer):
    points_array = PointEntrySerializer(many=True)


class AddTeamPointsSerializer(serializers.Serializer):
    matches = AddPointsSerializer(many=True)
    team_id = serializers.IntegerField(required=True)
    points = serializers.IntegerField(required=True)
    expired_date = serializers.DateTimeField(required=True)