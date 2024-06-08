from rest_framework import serializers
from applicant.models import Applicant
from applicant_info.models import ApplicantInfo
from competition.models import Competition
from matchtype.models import MatchType
from participant.models import Participant
from participant_info.models import ParticipantInfo
from tier.models import Tier
from users.models import CustomUser


class CompetitionListSerializer(serializers.ModelSerializer):
    tier = serializers.SerializerMethodField()
    match_type = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ('id', 'name', 'tier', 'match_type', 'start_date', 'status',
                  'location', 'phone', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'status')

    def get_tier(self, obj):
        return {'id': obj.tier.id, 'name': obj.tier.name} if obj.tier else None

    def get_match_type(self, obj):
        return {'id': obj.match_type.id,
                'gender': obj.match_type.gender,
                'type': obj.match_type.type} if obj.match_type else None


class CompetitionSerializer(serializers.ModelSerializer):
    tier = serializers.SerializerMethodField()
    tier_id = serializers.PrimaryKeyRelatedField(
        queryset=Tier.objects.all(), write_only=True, source='tier')
    match_type = serializers.SerializerMethodField()
    match_type_id = serializers.PrimaryKeyRelatedField(
        queryset=MatchType.objects.all(), write_only=True, source='match_type')
    image_file = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)
    delete_image = serializers.BooleanField(
        write_only=True, required=False, default=False)

    def get_image_url(self, obj):
        return obj.image_url.image_url if obj.image_url else None

    def get_tier(self, obj):
        return {'id': obj.tier.id, 'name': obj.tier.name} if obj.tier else None

    def get_match_type(self, obj):
        return {'id': obj.match_type.id,
                'gender': obj.match_type.gender,
                'type': obj.match_type.type} if obj.match_type else None

    class Meta:
        model = Competition
        fields = ('id', 'name', 'description', 'start_date', 'end_date', 'status',
                  'total_rounds', 'total_sets', 'rule', 'address', 'location', 'code',
                  'phone', 'fee', 'bank_name', 'bank_account_number', 'bank_account_name',
                  'site_link', 'image_file', 'image_url', 'match_type', 'match_type_id',
                  'tier', 'tier_id', 'max_participants', 'competition_type',
                  'created_at', 'updated_at', 'delete_image')
        read_only_fields = ('id', 'created_at', 'updated_at', 'status', 'code')
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
            'end_date': {'required': False},
            'total_rounds': {'required': False},
            'rule': {'required': False, 'allow_blank': True},
            'address': {'required': False, 'allow_blank': True},
            'location': {'required': False, 'allow_blank': True},
            'phone': {'required': False, 'allow_blank': True},
            'fee': {'required': False},
            'bank_name': {'required': False, 'allow_blank': True},
            'bank_account_number': {'required': False, 'allow_blank': True},
            'bank_account_name': {'required': False, 'allow_blank': True},
            'site_link': {'required': False, 'allow_blank': True},
            'max_participants': {'required': False},
            'delete_image': {'write_only': True},
            'tier': {'required': False},
            'tier_id': {'required': False},
        }


class CompetitionUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username')


class ApplicantSerializer(serializers.ModelSerializer):
    user = CompetitionUserSerializer(read_only=True)

    class Meta:
        model = Applicant
        fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation['user']


class ApplicantInfoSerializer(serializers.ModelSerializer):
    applicants = ApplicantSerializer(many=True, read_only=True)
    has_payment = serializers.BooleanField()
    has_refund = serializers.BooleanField()

    class Meta:
        model = ApplicantInfo
        fields = ('id', 'status', 'expired_date',
                  'competition', 'waiting_number', 'applicants', 'created_at', 'updated_at', 'has_payment', 'has_refund')
        read_only_fields = ('id', 'waiting_number',
                            'competition', 'expired_date', 'status', 'applicants', 'created_at', 'updated_at')
        extra_kwargs = {
            'expired_date': {'required': False},
            'waiting_number': {'required': False},
        }


class ParticipantSerializer(serializers.ModelSerializer):
    user = CompetitionUserSerializer()

    class Meta:
        model = Participant
        fields = ['user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation['user']


class ParticipantInfoSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = ParticipantInfo
        fields = ('id', 'participants', 'competition',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'competition', 'participants',
                            'created_at', 'updated_at')
