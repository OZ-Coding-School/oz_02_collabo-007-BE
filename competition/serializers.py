from django.utils.timezone import now
from rest_framework import serializers
from .models import Competition, CompetitionResult
from applicant.models import Applicant
from participant.models import Participant
from applicant_info.models import ApplicantInfo
from matchtype.serializers import MatchTypeSerializer
from image_url.serializers import ImageUrlSerializer
from participant.serializers import ParticipantSerializer
from match.serializers import MyCompetitionMatchSerializer
from match.models import Match
from django.db.models import Q




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
        current_applicants_count = obj.applicants.filter(status__in=['unpaid', 'confirmed_participation'], waiting_number__isnull=True).count()
        current_waiting_applicants_count = obj.applicants.filter(status__in=['unpaid', 'pending_participation'], waiting_number__isnull=False).count()

        
        ## 대회 리스트에서 버튼 구현을 위한 조건문 로직
        ## 대회 전 / 유저의 조건에 따라 신청 가능여부 판별
        # 로그인 x 상태일 때
        if obj.status == 'before' and not user.is_authenticated:
            return 'Registration Unavailable'
        # 로그인 확인
        if obj.status == 'before':
            # 신청 여부 확인
            if Applicant.objects.filter(user=user, applicant_info__competition=obj, applicant_info__status__in=['unpaid', 'pending_participation', 'confirmed_participation']).exists():
                return 'Registration Confirmed' # 신청완료
            # 유저 성별 / 실력 확인
            if (user.gender != obj.match_type.gender and obj.match_type.gender != 'mix')  or obj.tier not in user.tiers.all():
                return 'Registration Unavailable' # 신청불가
            # 대기 상태 여부
            elif current_applicants_count >= obj.max_participants:
                return 'Waitlist Available' # 대기 가능
            # 모든 상황이 부합할 경우 신청 가능
            else:
                return 'Registration Available' # 신청 가능
        # 대회 진행중    
        elif obj.status == 'during':
            return 'during'
        # 대회 종료
        else:
            return 'ended'
        
    def get_waiting_count(self, obj):
        current_applicants_count = obj.applicants.filter(status__in=['unpaid', 'confirmed_participation', 'pending_participation']).count()
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
        current_applicants_count = obj.applicants.filter(status__in=['unpaid', 'confirmed_participation'], waiting_number__isnull=True).count()
        current_waiting_applicants_count = obj.applicants.filter(status__in=['unpaid', 'pending_participation'], waiting_number__isnull=False).count()
        
        ## 대회 리스트에서 버튼 구현을 위한 조건문 로직
        ## 대회 전 / 유저의 조건에 따라 신청 가능여부 판별
        # 로그인 x 상태일 때
        if obj.status == 'before' and not user.is_authenticated:
            return 'Registration Unavailable'
        # 로그인 확인
        if obj.status == 'before':
            # 신청 여부 확인
            if Applicant.objects.filter(user=user, applicant_info__competition=obj, applicant_info__status__in=['unpaid', 'pending_participation', 'confirmed_participation']).exists():
                return 'Registration Confirmed'
            # 유저 성별 / 실력 확인
            if (user.gender != obj.match_type.gender and obj.match_type.gender != 'mix')  or obj.tier not in user.tiers.all():
                return 'Registration Unavailable'
            # 대기 상태 여부
            elif current_applicants_count >= obj.max_participants:
                return 'Waitlist Available'
            # 모든 상황이 부합할 경우 신청 가능
            else:
                return 'Registration Available'
        # 대회 진행중    
        elif obj.status == 'during':
            return 'during'
        # 대회 종료
        else:
            return 'ended'
        
    def get_waiting_count(self, obj):
        current_applicants_count = obj.applicants.filter(status__in=['unpaid', 'confirmed_participation', 'pending_participation']).count()
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
        fields = ['name', 'start_date', 'match_type_details', 'tier', 'total_rounds', 'location', 'address', 'bank_account_name', 
                  'bank_name', 'bank_account_number', 'fee']
        
        
    def get_tier(self, obj):
        if obj.tier:
            return obj.tier.name
        return None
    


## 참가 신청한 대회 정보 
class MyCompetitionSerializer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()
    apply_status = serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    match_status = serializers.SerializerMethodField()
    myteam = serializers.SerializerMethodField()

    
    class Meta:
        model = Competition
        fields = ['id', 'name', 'start_date', 'tier', 'match_type_details', 'total_rounds', 'total_sets', 'location', 'address', 
                'description', 'rule', 'phone', 'site_link', 'image_url', 'status', 'apply_status','myteam','match_status','matches' ]
    
    def get_myteam(self, obj):
        
        user = self.context['request'].user

        myteam = Applicant.objects.filter(user=user,applicant_info__competition=obj).order_by('-created_at').first()

        if myteam :
            info = myteam.applicant_info

            myteam_all = Applicant.objects.filter(applicant_info=info)

            myteam1 = [myteamuser.user.username for myteamuser in myteam_all if myteamuser.user == user] 
            myteam2 = [myteamuser.user.username for myteamuser in myteam_all if myteamuser.user != user]
            myteamuser = myteam1+myteam2

        else:
            return None

        
        return myteamuser
        


    def get_match_status(self, obj):

        user = self.context['request'].user

        matches = Match.objects.filter(
            Q(a_team__participants__user=user) | Q(b_team__participants__user=user),
            competition=obj
        )

        # 유저의 applicant_info의 waiting_number
        applicant = Applicant.objects.filter(user=user,applicant_info__competition=obj).order_by('-created_at').first()

        if applicant:
            waiting_number = applicant.applicant_info.waiting_number
        else:
            waiting_number = None

        if waiting_number is not None:
            return 'pending_participation'

        if not matches :
            return 'unassigned_match_competitions'
        

    # matches 필드 추가
    def get_matches(self, obj):
        # 로그인한 사용자 정보 가져오기
        user = self.context['request'].user

        # 사용자가 속한 대회에 해당하는 매치 정보 가져오기
        matches = Match.objects.filter(
            Q(a_team__participants__user=user) | Q(b_team__participants__user=user),
            competition=obj
        ).order_by('-created_at')

        latest_match = matches.first()

        if latest_match:
            # 매치 정보를 시리얼화하여 반환
            return MyCompetitionMatchSerializer(latest_match, context={'request': self.context['request']}).data
        
        return None

    # applicant_info.status도 보여주기
    def get_apply_status(self, obj):
        user = self.context['request'].user

        applicant = Applicant.objects.filter(user=user,applicant_info__competition=obj).order_by('-created_at').first()
        
        if applicant:
            return applicant.applicant_info.status
        
        return None

    def get_tier(self, obj):
        if obj.tier:
            return obj.tier.name
        return None

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None



## 대회 결과 조회
class CompetitionResultSerializer(serializers.ModelSerializer):
    competition_name = serializers.SerializerMethodField()
    match_type_details = MatchTypeSerializer(source='competition.match_type', read_only=True)
    tier = serializers.SerializerMethodField()
    winner_participants = serializers.SerializerMethodField()
    runner_up_participants = serializers.SerializerMethodField()

    class Meta:
        model = CompetitionResult
        fields = ['competition', 'competition_name', 'match_type_details', 'tier', 'winner', 'winner_participants', 'runner_up', 'runner_up_participants']

    def get_competition_name(self, obj):
        return obj.competition.name

    def get_tier(self, obj):
        return obj.competition.tier.name if obj.competition.tier else None

    def get_winner_participants(self, obj):
        participants = Participant.objects.filter(participant_info=obj.winner)
        return ParticipantSerializer(participants, many=True).data

    def get_runner_up_participants(self, obj):
        participants = Participant.objects.filter(participant_info=obj.runner_up)
        return ParticipantSerializer(participants, many=True).data
