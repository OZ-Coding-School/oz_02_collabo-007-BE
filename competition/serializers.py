from django.utils.timezone import now
from rest_framework import serializers
from .models import Competition
from applicant_info.models import ApplicantInfo
from matchtype.serializers import MatchTypeSerializer
from image_url.serializers import ImageUrlSerializer




''' 대회 부분 '''

## 대회 리스트 조회
class CompetitionListSerializer(serializers.ModelSerializer):
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    image_url = serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    waiting_count = serializers.SerializerMethodField()
    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'end_date', 'match_type_details', 'tier', 'location', 'image_url', 'status', 'waiting_count']
        
    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    def get_tier(self, obj):
        if obj.tier:
            return obj.tier.name
        return None
    
    def get_status(self, obj):
        user = self.context['request'].user
        current_applicants_count = obj.applicants.count()
        is_waiting = current_applicants_count >= obj.max_participants
        
        ## 대회 전 / 유저의 조건에 따라 신청 가능여부 판별
        # 로그인 x 상태일 때
        if obj.status == 'before' and not user.is_authenticated:
            return '신청 불가능'
        # 로그인 확인
        if obj.status == 'before':
            # 유저 성별 / 실력 확인
            if (user.gender != obj.match_type.gender and obj.match_type.gender != 'mix')  or user.tier != obj.tier:
                return '신청 불가능'
            # 대기 상태 여부
            elif current_applicants_count >= obj.max_participants:
                return '대기 가능'
            # 모든 상황이 부합할 경우 신청 가능
            else:
                return '신청 가능'
        # 대회 진행중    
        elif obj.status == 'during':
            return '대회 진행중'
        # 대회 종료
        else:
            return '대회 종료'
        
    def get_waiting_count(self, obj):
        current_applicants_count = obj.applicants.count()
        if current_applicants_count - obj.max_participants < 0:
            return 0
        return current_applicants_count - obj.max_participants



## 대회 상세정보
class CompetitionDetailInfoSerializer(serializers.ModelSerializer):
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    image_url = serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    waiting_count = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'tier', 'match_type_details', 'total_rounds', 'total_sets', 'location', 'address', 
                  'description', 'rule', 'phone', 'site_link', 'image_url', 'status', 'waiting_count']
    
    
    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None
    
    def get_tier(self, obj):
        if obj.tier:
            return obj.tier.name
        return None
    
    def get_status(self, obj):
        user = self.context['request'].user
        current_applicants_count = obj.applicants.count()
        is_waiting = current_applicants_count >= obj.max_participants
        
        ## 대회 전 / 유저의 조건에 따라 신청 가능여부 판별
        # 로그인 x 상태일 때
        if obj.status == 'before' and not user.is_authenticated:
            return '신청 불가능'
        # 로그인 확인
        if obj.status == 'before':
            # 유저 성별 / 실력 확인
            if (user.gender != obj.match_type.gender and obj.match_type.gender != 'mix')  or user.tier != obj.tier:
                return '신청 불가능'
            # 대기 상태 여부
            elif current_applicants_count >= obj.max_participants:
                return '대기 가능'
            # 모든 상황이 부합할 경우 신청 가능
            else:
                return '신청 가능'
        # 대회 진행중    
        elif obj.status == 'during':
            return '대회 진행중'
        # 대회 종료
        else:
            return '대회 종료'
        
    def get_waiting_count(self, obj):
        current_applicants_count = obj.applicants.count()
        if current_applicants_count - obj.max_participants < 0:
            return 0
        return current_applicants_count - obj.max_participants



## 대회 간단정보
class CompetitionApplyInfoSerializer(serializers.ModelSerializer):
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    
    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'match_type_details', 'total_rounds', 'total_sets', 'location', 'address', 'code' ]



## 대회신청        
class CompetitionApplySerializer(serializers.ModelSerializer):
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    tier = serializers.SerializerMethodField()
    
    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'match_type_details', 'tier', 'total_rounds', 'total_sets', 'location', 'address', 'bank_account_name', 
                  'bank_name', 'bank_account_number', 'fee']
        
        
    def get_tier(self, obj):
        if obj.tier:
            return obj.tier.name
        return None
    


## 대회 현황
class CompetitionStatusSerializer(serializers.ModelSerializer):
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    
    
    class Meta:
        fields = ['name', 'match_type_details', 'tier', ]