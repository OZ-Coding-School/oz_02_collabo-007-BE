from rest_framework import serializers
from .models import Match
from participant.models import Participant
from users.serializers import UserInfoSerializer
from set.serializers import SetSerializer
from set.models import Set
from users.models import CustomUser
from django.db.models import Q

class MatchSerializer(serializers.ModelSerializer):
    sets = serializers.SerializerMethodField()
    a_team_users = serializers.SerializerMethodField()
    b_team_users = serializers.SerializerMethodField()
    winner_user = serializers.SerializerMethodField()
    match_round = serializers.IntegerField(allow_null=True)
    total_sets = serializers.SerializerMethodField()
    
    class Meta:
        model = Match
        fields = ['id', 'match_round', 'match_number', 'court_number', 'total_sets', 'description', 'winner_user', 'a_team_users', 'b_team_users', 'sets']

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

    def get_total_sets(self, obj):
        return obj.competition.total_sets


class MyCompetitionMatchSerializer(serializers.ModelSerializer):
    
    winner_name = serializers.SerializerMethodField()
    myteam_user = serializers.SerializerMethodField()
    opponent_user = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['id', 'match_round', 'match_number', 'court_number', 'winner_name', 'myteam_user', 'opponent_user']


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
    
    def get_myteam_user(self, obj):
        user = self.context['request'].user
        a_team_users = self.get_a_team_user(obj)
        b_team_users = self.get_b_team_user(obj)

        if a_team_users and user.username in a_team_users:
            return a_team_users
        elif b_team_users and user.username in b_team_users:
            return b_team_users
        return None

    def get_opponent_user(self, obj):
        user = self.context['request'].user
        a_team_users = self.get_a_team_user(obj)
        b_team_users = self.get_b_team_user(obj)

        if a_team_users and user.username in a_team_users:
            return b_team_users
        elif b_team_users and user.username in b_team_users:
            return a_team_users
        return None


class MatchRecordSerializer(serializers.ModelSerializer):
    user_record = serializers.SerializerMethodField()
    user_matches = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'user_record', 'user_matches']
    
    def get_user_matches(self, obj):
        user_id = obj.id
        user_participants = Participant.objects.filter(user_id=user_id)
        user_matches_data = []
        
        for participant in user_participants:
            competition = participant.participant_info.competition
            competition_data = {
                'name': str(competition.name),
                'match_type_details': {
                    'gender': competition.match_type.gender,
                    'type': competition.match_type.type
                },
                'tier': str(competition.tier),
                'start': competition.start_date }
            user_matches = Match.objects.filter(Q(a_team=participant.participant_info) | Q(b_team=participant.participant_info))
            matches_data = MatchSerializer(user_matches, many=True).data
            competition_data['matches'] = matches_data
            user_matches_data.append(competition_data)
        return user_matches_data
    
    def get_user_record(self, obj):
        user_id = obj.id
        user_matches = self.get_user_matches(obj)
        matches = sum(len(match['matches']) for match in user_matches)
        wins = sum(1 for match in user_matches for match_data in match['matches'] if match_data.get('winner_user') and user_id in [user['id'] for user in match_data['winner_user']])
        losses = matches - wins
        return {'wins': wins, 'losses': losses}
    