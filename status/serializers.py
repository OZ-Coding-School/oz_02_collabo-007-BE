from rest_framework import serializers
from .models import Set
from match.models import Match
from participant.models import Participant
from users.serializers import UserInfoSerializer


        


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['id','setnumber', 'scorea', 'scoreb']

class MatchSerializer(serializers.ModelSerializer):
    sets = serializers.SerializerMethodField()
    competition_name = serializers.SerializerMethodField()
    a_team_users = serializers.SerializerMethodField()
    b_team_users = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['id', 'matchround', 'matchnumber', 'courtnumber', 'description', 'winner_id', 'competition_name', 'a_team_users', 'b_team_users', 'sets']

    def get_sets(self, obj):
        sets = Set.objects.filter(match_list=obj)
        return SetSerializer(sets, many=True).data

    def get_competition_name(self, obj):
        return obj.competiton.name if obj.competiton else None

    def get_a_team_users(self, obj):
        participants = Participant.objects.filter(participant_info=obj.a_team)
        return UserInfoSerializer([participant.user for participant in participants], many=True).data 

    def get_b_team_users(self, obj):
        participants = Participant.objects.filter(participant_info=obj.b_team)
        return UserInfoSerializer([participant.user for participant in participants], many=True).data  

