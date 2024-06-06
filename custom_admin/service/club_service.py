from club_applicant.models import ClubApplicant
from django.contrib.auth import get_user_model
from django.db import transaction

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
