from django.db import models
from core.models import TimeStampedModel
from team.models import Team
from matchtype.models import MatchType
from tier.models import Tier
from users.models import CustomUser
from match.models import Match, TeamMatch


class Point(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    points = models.IntegerField(blank=True, null=True)
    expired_date = models.DateTimeField(blank=True, null=True)
    tier = models.ForeignKey(Tier, models.DO_NOTHING, blank=True, null=True)
    team = models.ForeignKey(Team, models.DO_NOTHING, blank=True, null=True)
    match_type = models.ForeignKey(
        MatchType, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(
        CustomUser, models.DO_NOTHING, blank=True, null=True)
    match = models.ForeignKey(Match, models.DO_NOTHING, blank=True, null=True)
    team_match = models.ForeignKey(
        TeamMatch, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'point'
