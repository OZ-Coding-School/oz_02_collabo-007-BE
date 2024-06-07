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


class MyCompetitionMatchSerializer(serializers.ModelSerializer):
    
    winner_name = serializers.SerializerMethodField()
    a_team_user = serializers.SerializerMethodField()
    b_team_user = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['id', 'matchround', 'matchnumber', 'courtnumber', 'winner_name', 'a_team_user', 'b_team_user']


    def get_winner_name(self, obj):
        winner_info = obj.winner_id
        if winner_info:
            winners = Participant.objects.filter(participant_info=winner_info)
            if winners.exists():
                winner = [winner_member.user.username for winner_member in winners]
                return winner

        return None

    def get_a_team_user(self, obj):
        a_team_info = obj.a_team_id
        if a_team_info:
            a_team = Participant.objects.filter(participant_info=a_team_info)
            if a_team.exists() :
                a_team_users = [a_team_member.user.username for a_team_member in a_team]
                return a_team_users
        return None

    def get_b_team_user(self, obj):
        b_team_info = obj.b_team_id
        if b_team_info:
            b_team = Participant.objects.filter(participant_info=b_team_info)
            if b_team.exists():
                b_team_users = [b_team_member.user.username for b_team_member in b_team]
                return b_team_users
        return None