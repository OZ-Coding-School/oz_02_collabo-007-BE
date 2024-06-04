from faker import Faker
import random
from point.models import Point
from point.models import Tier, Team, MatchType, CustomUser  # 필요한 모델 임포트

fake = Faker()

def create_dummy_data(n):
    for _ in range(n):
        tier = random.choice(Tier.objects.all()) if Tier.objects.exists() else None
        team = random.choice(Team.objects.all()) if Team.objects.exists() else None
        match_type = random.choice(MatchType.objects.all()) if MatchType.objects.exists() else None
        user = random.choice(CustomUser.objects.all()) if CustomUser.objects.exists() else None

        Point.objects.create(
            points=random.randint(1, 100),
            expired_date=fake.date_time_between(start_date='-30d', end_date='+30d'),
            tier=tier,
            team=team,
            match_type=match_type,
            user=user,
        )

# 예를 들어 10개의 더미 데이터를 생성하려면 아래 함수를 호출하세요.
create_dummy_data(2)