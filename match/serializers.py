from rest_framework import serializers
from .models import Match
from participant.models import Participant
from users.serializers import UserInfoSerializer
from set.serializers import SetSerializer
from set.models import Set



class MatchSerializer(serializers.ModelSerializer):
    sets = serializers.SerializerMethodField()
    competition_name = serializers.SerializerMethodField()
    a_team_users = serializers.SerializerMethodField()
    b_team_users = serializers.SerializerMethodField()
    winner_user = serializers.SerializerMethodField()
    class Meta:
        model = Match
        fields = ['id', 'matchround', 'matchnumber', 'courtnumber', 'description', 'winner_user', 'competition_name', 'a_team_users', 'b_team_users', 'sets']

    def get_sets(self, obj):
        sets = Set.objects.filter(match_list=obj)
        return SetSerializer(sets, many=True).data

    def get_competition_name(self, obj):
        return obj.competition.name if obj.competition else None
    
    def get_winner_user(self, obj):
        participants = Participant.objects.filter(participant_info=obj.winner_id)
        return UserInfoSerializer([participant.user for participant in participants], many=True).data 

    def get_a_team_users(self, obj):
        participants = Participant.objects.filter(participant_info=obj.a_team)
        return UserInfoSerializer([participant.user for participant in participants], many=True).data 

    def get_b_team_users(self, obj):
        participants = Participant.objects.filter(participant_info=obj.b_team)
        return UserInfoSerializer([participant.user for participant in participants], many=True).data  