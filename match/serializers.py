from rest_framework import serializers
from .models import Match
from participant.models import Participant
from users.serializers import UserInfoSerializer
from set.serializers import SetSerializer
from set.models import Set



class MatchSerializer(serializers.ModelSerializer):
    sets = serializers.SerializerMethodField()
    a_team_users = serializers.SerializerMethodField()
    b_team_users = serializers.SerializerMethodField()
    winner_user = serializers.SerializerMethodField()
    class Meta:
        model = Match
        fields = ['id', 'match_round', 'match_number', 'court_number', 'description', 'winner_user', 'a_team_users', 'b_team_users', 'sets']

    def get_sets(self, obj):
        sets = Set.objects.filter(match_list=obj)
        return SetSerializer(sets, many=True).data if sets.exists() else None
    
    def get_winner_user(self, obj):
        participants = Participant.objects.filter(participant_info=obj.winner_id)
        users_data = UserInfoSerializer([participant.user for participant in participants], many=True).data
        return users_data if users_data else None

    def get_a_team_users(self, obj):
        participants = Participant.objects.filter(participant_info=obj.a_team)
        users_data = UserInfoSerializer([participant.user for participant in participants], many=True).data
        return users_data if users_data else None

    def get_b_team_users(self, obj):
        participants = Participant.objects.filter(participant_info=obj.b_team)
        users_data = UserInfoSerializer([participant.user for participant in participants], many=True).data
        return users_data if users_data else None
