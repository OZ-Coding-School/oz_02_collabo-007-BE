from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model , authenticate
from rest_framework import serializers
from .models import Club, CustomUser
from image_url.models import ImageUrl
from image_url.utils import S3ImageUploader
from club.serializers import ClubDetailSerializer
from club_applicant.models import ClubApplicant
from team.serializers import TeamDetailSerializer
from club_applicant.serializers import ClubApplicantSerializer
from point.models import Point
from matchtype.serializers import MatchTypeSerializer


User = get_user_model()

# 회원가입 부분
class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all(), required=False)
    image_file = serializers.ImageField(write_only=True, required=False, allow_null=True)  # 이미지 필드 추가
    image_url = serializers.SerializerMethodField(read_only=True)  # 읽기 전용 이미지 URL 필드 추가
    
    class Meta:
        model = User
        fields = ('phone', 'password', 'username', 'birth', 'gender', 'club', 'image_file', 'image_url')
        
    def validate_phone(self, value):
        # 숫자로만 구성되어 있는지 확인
        if not value.isdigit():
            raise serializers.ValidationError("휴대폰 번호는 숫자만 포함해야 합니다.")
        return value
        

    def create(self, validated_data):
        club_data = validated_data.pop('club', None)
        image_data = validated_data.pop('image_file', None)
        user = User.objects.create_user(
            phone=validated_data['phone'],
            password=validated_data['password'],
            username=validated_data['username'],
            birth=validated_data.get('birth'),
            gender=validated_data.get('gender'),
        )
        
        # 클럽 가입 신청 처리
        if club_data:
            ClubApplicant.objects.create(user=user, club=club_data)

        # image_data가 None이 아니고, 파일 크기가 0보다 큰 경우에만 이미지 업로드 실행
        if image_data and hasattr(image_data, 'size') and image_data.size > 0:
            uploader = S3ImageUploader()
            file_url, extension, size = uploader.upload_file(image_data)
            
            # 업로드된 이미지 정보를 ImageUrl 인스턴스로 저장
            image_instance = ImageUrl.objects.create(
                image_url=file_url,
                extension=extension,
                size=size
            )
            user.image_url = image_instance  # 사용자 인스턴스에 이미지 인스턴스 할당
            
        user.save()  # 변경 사항 저장

            
        return user
    
    
    
    
# 휴대폰 번호 중복 체크 serializer

class PhoneCheckSerializer(serializers.Serializer):
    phone = serializers.CharField()
    
    def validate_phone(self, value):
        # 숫자로만 구성되어 있는지 확인
        if not value.isdigit():
            raise serializers.ValidationError("휴대폰 번호는 숫자만 포함해야 합니다.")
        
        # 이미 사용 중인지 확인
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("이미 사용 중인 휴대폰 번호입니다.")
        
        return value






# 로그인 부분 serializer ##

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'phone'
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['phone'] = user.phone
        
        return token

    def validate(self, attrs):
        # 'username' 대신 'phone'을 사용하여 인증
        authenticate_kwargs = {
            'phone': attrs.get(self.username_field),
            'password': attrs.get('password'),
        }
        
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None or not self.user.is_active:
            raise serializers.ValidationError('로그인에 실패하였습니다. 전화번호와 비밀번호를 확인해 주세요.')
        
        # 토큰 발급
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        
        
        return data




# 회원정보 수정 serializer
class UpdateMyProfileSerializer(serializers.ModelSerializer):
    club = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    image_file = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(read_only=True)
    remove_image = serializers.BooleanField(write_only=True, required=False, default=False) # 기존 이미지 삭제를 위한 필드 정의!

    class Meta:
        model = User
        fields = ('username', 'birth', 'gender', 'club', 'image_file', 'image_url', 'remove_image')

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    def update(self, instance, validated_data):
        image_data = validated_data.pop('image_file', None)
        remove_image = validated_data.pop('remove_image', False)

        # 사용자 기본 정보 업데이트
        instance.username = validated_data.get('username', instance.username)
        instance.birth = validated_data.get('birth', instance.birth)
        instance.gender = validated_data.get('gender', instance.gender)


        # 클럽 ID 처리
        club_data = validated_data.pop('club', None)
        
        # 빈 문자열 - 프로필 편집에서 유저가 기존 클럽을 삭제한 경우 (유저의 클럽id를 Null으로 변경)
        if club_data in ['']:  
            instance.club = None
            instance.team = None
        
        # request 폼데이터에 클럽 데이터가 제공되지 않은 경우 (기존 클럽 유지)
        elif club_data is None: 
            pass
            
        else:
            try:
                # 클럽을 변경 신청한 경우
                club_instance = Club.objects.get(id=club_data)
                
                # 기존에 유저가 가지고 있던 클럽id를 null값으로 변경
                instance.club = None
                
                # 기존에 유저가 가지고 있던 팀id를 null값으로 변경
                instance.team = None
                
                instance.save()
                
                # 새로운 클럽에 가입 신청
                ClubApplicant.objects.create(user=instance, club=club_instance)
                
            except Club.DoesNotExist:
                raise serializers.ValidationError('해당 클럽이 존재하지 않습니다')


        # 이미지 파일 처리    
        if remove_image: # 클라이언트가 이미지 제거를 요청한 경우
            instance.image_url = None
            
        elif image_data is None: # 폼데이터에 이미지 파일 자체가 제공되지 않은 경우
            pass
        
        else:
            # 이미지 업로드 로직
            uploader = S3ImageUploader()
            file_url, extension, size = uploader.upload_file(image_data)
            if hasattr(instance, 'image_url') and instance.image_url:
                # 기존 이미지 업데이트
                instance.image_url.image_url = file_url
                instance.image_url.extension = extension
                instance.image_url.size = size
                instance.image_url.save()
            else:
                # 새 이미지 생성
                image_instance = ImageUrl.objects.create(
                    image_url=file_url,
                    extension=extension,
                    size=size
                )
                instance.image_url = image_instance

        instance.save()
        return instance




# 비밀번호 변경 시리얼라이저
class ChangePasswordSerializer(serializers.Serializer):
    prev_password = serializers.CharField(required=True)  # 기존 비밀번호
    changed_password = serializers.CharField(required=True)  # 변경 비밀번호
    

    
    class Meta:
        model = User
        fields = ['password']
        







# 유저 상세정보 serializer
class UserInfoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    tiers = serializers.SerializerMethodField()
    club = serializers.SerializerMethodField()
    team = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'gender', 'birth', 'image_url', 'tiers', 'club', 'team'] # 티어 추가해야함

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None
    
    def get_tiers(self, obj):
        tiers = obj.tiers.all()  # users-tiers 다대다 관계라 연결된 모든 티어를 가져옴
        return [{
            'id': tier.id,
            'name': tier.name,
            'match_type_detail': {
                'gender': tier.match_type.gender,
                'type': tier.match_type.type
            }
        } for tier in tiers]


    def get_club(self, obj):
        # 유저가 클럽 오브젝트를 가지고 있는 경우
        if obj.club:
            club = obj.club
            return {
                'id': club.id,
                'name': club.name,
                'image_url': club.image_url.image_url if club.image_url else None
            }
        # 유저가 클럽 오브젝트를 가지고 있지 않은 경우
        else:
            # 가장 최근의 ClubApplicant 1개만 가져옴
            club_applicant = ClubApplicant.objects.filter(user=obj).order_by('-date_applied').first()
            # applicant status 가 pending 상태 일 경우에만 데이터 리턴
            if club_applicant and club_applicant.status == 'pending':
                return {
                    'id': club_applicant.club.id,
                    'name': club_applicant.club.name,
                    'image_url': club_applicant.club.image_url.image_url if club_applicant.club.image_url else None,
                    'status': club_applicant.status,
                    'date_applied': club_applicant.date_applied
                }
            else:
                return None
    
    
    
    def get_team(self, obj):
        if obj.team:
            team = obj.team
            return {
                'id': team.id,
                'name': team.name,
                'image_url': team.image_url.image_url if team.image_url else None       
            }
            
        return None



# 내 프로필 랭킹조회 serializer
class MyProfileRankingSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    user= serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()

    class Meta:
        model = Point
        fields = ('match_type_details', 'rank', 'total_points', 'user', 'tier')

     # 각 필드 이름 가져오는 인스턴스 메서드
    def get_user(self, obj):
        user = obj.get('user')
        if user:
            return {
                'id': user.id,
                'username': user.username,
            }
        return None


    def get_tier(self, obj):
        tier = obj.get('tier')
        if tier:
            return {
                'id': tier.id,
                'name': tier.name,
                'match_type_details': {
                    'gender': tier.match_type.gender,
                    'type': tier.match_type.type
                }
            }
        return None
    


    
# 내 프로필 팀 랭킹 조회 serializer
class MyProfileTeamRankingSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    team= serializers.SerializerMethodField()

    class Meta:
        model = Point
        fields = ('match_type_details', 'rank', 'total_points', 'team')

    # 각 필드 이름 가져오는 인스턴스 메서드
    def get_team(self, obj):
        team = obj['team']
        if team:
            return {
                'id': team.id,
                'name': team.name,
            }
        return None

        
        
# 대표 랭킹 serializer
class MainRankingSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = CustomUser
        fields = ('main_ranking',)






# 파트너 검색용 시리얼라이저
class UserWithClubInfoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    club = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'image_url', 'club')

    def get_image_url(self, obj):
        if obj.image_url:
            return obj.image_url.image_url
        return None

    def get_club(self, obj):
        if obj.club:
            return {
                'id': obj.club.id,
                'name': obj.club.name
            }
        return None
    
    
    
    
    
# 특정 유저 랭킹조회 serializer
class UserRankingSearchSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    user= serializers.SerializerMethodField()
    tier = serializers.SerializerMethodField()

    class Meta:
        model = Point
        fields = ('match_type_details', 'rank', 'total_points', 'user', 'tier')

     # 각 필드 이름 가져오는 인스턴스 메서드
    def get_user(self, obj):
        user = obj.get('user')
        if user:
            return {
                'id': user.id,
                'username': user.username,
            }
        return None


    def get_tier(self, obj):
        tier = obj.get('tier')
        if tier:
            return {
                'id': tier.id,
                'name': tier.name,
                'match_type_details': {
                    'gender': tier.match_type.gender,
                    'type': tier.match_type.type
                }
            }
        return None
    
    
    
    
    
    

# 특정 유저의 팀 랭킹 조회 serializer
class UserTeamRankingSearchSerializer(serializers.ModelSerializer):
    total_points = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)
    match_type_details = MatchTypeSerializer(source='match_type', read_only=True)
    team= serializers.SerializerMethodField()

    class Meta:
        model = Point
        fields = ('match_type_details', 'rank', 'total_points', 'team')

    # 각 필드 이름 가져오는 인스턴스 메서드
    def get_team(self, obj):
        team = obj.get('team')
        if team:
            return {
                'id': team.id,
                'name': team.name,
            }
        return None