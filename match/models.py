from django.db import models
from core.models import TimeStampedModel, SoftDeleteModel
from competition.models import Competition
from participant_info.models import ParticipantInfo, TeamParticipantInfo


class BaseMatch(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)
    # Field name made lowercase.
    match_round = models.IntegerField(blank=True, null=True)
    # Field name made lowercase.
    match_number = models.IntegerField(blank=True, null=True)
    # Field name made lowercase.
    court_number = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class Match(BaseMatch):
    winner_id = models.ForeignKey(
        ParticipantInfo, models.DO_NOTHING, related_name='winner_user', blank=True, null=True)
    competition = models.ForeignKey(
        Competition, models.DO_NOTHING, related_name='matches')
    a_team = models.ForeignKey(ParticipantInfo, models.DO_NOTHING,
                               related_name='match_a_team_set', blank=True, null=True)
    b_team = models.ForeignKey(ParticipantInfo, models.DO_NOTHING,
                               related_name='match_b_team_set', blank=True, null=True)
    total_sets = models.IntegerField(blank=True, null=True)
    team_match = models.ForeignKey(
        'TeamMatch', models.DO_NOTHING, blank=True, null=True, related_name='matches')
    team_match_game_number = models.IntegerField(
        blank=True, null=True, help_text="팀 게임 내 경기 번호")

    class Meta:
        db_table = 'match'
        ordering = ['match_number']


class TeamMatch(BaseMatch):
    winner = models.ForeignKey(
        TeamParticipantInfo, models.DO_NOTHING, related_name='winner_team', blank=True, null=True)
    a_team = models.ForeignKey(TeamParticipantInfo, models.DO_NOTHING,
                               related_name='a_team', blank=True, null=True)
    b_team = models.ForeignKey(TeamParticipantInfo, models.DO_NOTHING,
                               related_name='b_team', blank=True, null=True)
    competition = models.ForeignKey(
        Competition, models.DO_NOTHING, related_name='team_matches')
    a_team_score = models.IntegerField(blank=True, null=True)
    b_team_score = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'team_match'
