from django.db import models
from applicant_info.models import ApplicantInfo, TeamApplicantInfo
from core.models import TimeStampedModel, SoftDeleteModel
from competition.models import Competition
from team.models import Team


class BaseParticipantInfo(TimeStampedModel, SoftDeleteModel):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.id} / {self.competition.name}"

    class Meta:
        abstract = True


class ParticipantInfo(BaseParticipantInfo):
    competition = models.ForeignKey(
        Competition, on_delete=models.DO_NOTHING, related_name='participants')
    applicant_info = models.OneToOneField(
        ApplicantInfo, related_name='participant_info', on_delete=models.DO_NOTHING, null=True, blank=True)
    team_participant_info = models.OneToOneField(
        'TeamParticipantInfo',  on_delete=models.DO_NOTHING, null=True, blank=True)
    team_participant_game_number = models.IntegerField(
        blank=True, null=True, help_text="팀 게임 내 경기 번호")

    class Meta:
        db_table = 'participant_info'


class TeamParticipantInfo(BaseParticipantInfo):
    competition = models.ForeignKey(
        Competition, on_delete=models.DO_NOTHING, related_name='team_participants')
    team_applicant_info = models.OneToOneField(
        TeamApplicantInfo, related_name='team_participant_info', on_delete=models.DO_NOTHING, null=True, blank=True)
    team = models.ForeignKey(
        Team, on_delete=models.DO_NOTHING, related_name='team_participants')

    class Meta:
        db_table = 'team_participant_info'
