from club_applicant.models import ClubApplicant
from django.contrib.auth import get_user_model
from django.db import transaction

from team.models import Team
from tier.models import Tier
from users.models import CustomUser

User = get_user_model()


class ClubService:

    def accept_club_application(self, club_applicant: ClubApplicant):
        with transaction.atomic():
            club_applicant.accept()
            user = club_applicant.user
            user.set_club(club_applicant.club)

        return club_applicant

    def reject_club_application(self, club_applicant: ClubApplicant):
        club_applicant.reject()
        return club_applicant

    def update_member(self, user: CustomUser, member_data: dict):
        with transaction.atomic():
            self._update_team(user, member_data.get('team_id'))
            self._update_tier(user, member_data.get('single_tier_id'), 'single')
            self._update_tier(user, member_data.get('double_tier_id'), 'double')

            user.save()
        return user

    def _update_team(self, user: CustomUser, team_id: int):
        with transaction.atomic():
            try:
                team = Team.objects.get(id=team_id)
                user.team = team
                user.save()
            except Team.DoesNotExist:
                raise ValueError(f"팀 id {team_id}가 존재하지 않습니다")
        return user

    def _update_tier(self, user: CustomUser, tier_id: int, tier_type: str):
        if tier_id is not None:
            if tier_id == '':
                user.tiers.remove(
                    *user.tiers.filter(match_type__type=tier_type))
            else:
                try:
                    tier = Tier.objects.get(id=tier_id)
                    self._validate_tier(tier, user, tier_type)
                    user.tiers.remove(
                        *user.tiers.filter(match_type__type=tier_type))
                    user.tiers.add(tier)
                except Tier.DoesNotExist:
                    raise ValueError(f"{tier_type.capitalize()} 부가 존재하지 않습니다")

    def _validate_tier(self, tier: Tier, user: CustomUser, tier_type: str):
        if tier.match_type.gender != user.gender:
            raise ValueError(f"{tier_type.capitalize()} 부의 성별이 다릅니다.")
        if tier.match_type.type != tier_type:
            raise ValueError(f"{tier_type.capitalize()} 부가 아닙니다.")
