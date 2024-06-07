from rest_framework import serializers
from .models import Set
from match.models import Match
from participant.models import Participant
from users.serializers import UserInfoSerializer


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['id','set_number', 'a_score', 'b_score']



