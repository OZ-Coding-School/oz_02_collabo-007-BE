from rest_framework import serializers
from competition.models import Competition


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
    image_file = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField(read_only=True)
    delete_image = serializers.BooleanField(
        write_only=True, required=False, default=False)

    def get_image_url(self, obj):
        return obj.image_url.image_url if obj.image_url else None

    class Meta:
        model = Competition
        fields = ('id', 'name', 'description', 'start_date', 'end_date', 'status',
                  'total_rounds', 'total_sets', 'rule', 'address', 'location', 'code',
                  'phone', 'fee', 'bank_name', 'bank_account_number', 'bank_account_name',
                  'site_link', 'image_file', 'image_url', 'match_type', 'tier', 'max_participants',
                  'created_at', 'updated_at', 'delete_image')
        read_only_fields = ('id', 'created_at', 'updated_at', 'status', 'code')
