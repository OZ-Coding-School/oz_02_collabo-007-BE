# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class Club(models.Model):
#     id = models.IntegerField(primary_key=True)
#     address = models.CharField(max_length=100, blank=True, null=True)
#     phone = models.CharField(max_length=30, blank=True, null=True)
#     name = models.CharField(max_length=30, blank=True, null=True)
#     description = models.CharField(max_length=100, blank=True, null=True)
#     image_url = models.ForeignKey('ImageUrl', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'club'


# class Coach(models.Model):
#     id = models.IntegerField(primary_key=True)
#     club = models.ForeignKey(Club, models.DO_NOTHING)
#     user = models.ForeignKey('Users', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'coach'


# class Competition(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=30, blank=True, null=True)
#     status = models.CharField(max_length=6, blank=True, null=True)
#     startdate = models.DateTimeField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
#     enddate = models.DateTimeField(db_column='endDate', blank=True, null=True)  # Field name made lowercase.
#     round = models.IntegerField(blank=True, null=True)
#     description = models.CharField(max_length=100, blank=True, null=True)
#     rule = models.TextField(blank=True, null=True)
#     address = models.CharField(max_length=100, blank=True, null=True)
#     location = models.CharField(max_length=30, blank=True, null=True)
#     code = models.BigIntegerField(blank=True, null=True)
#     phone = models.CharField(max_length=30, blank=True, null=True)
#     fee = models.IntegerField(blank=True, null=True) # 대회 참가비 변수명 바꿔야할듯
#     bank_name = models.CharField(db_column='bankName', max_length=30, blank=True, null=True) 
#     bank_account_number = models.IntegerField(db_column='bankAccountNumber', blank=True, null=True)  
#     bank_account_name = models.CharField(db_column='bankAccountName', max_length=30, blank=True, null=True)  
#     site_link = models.TextField(db_column='siteLink', blank=True, null=True)  
#     feedback = models.CharField(max_length=255, blank=True, null=True)
#     match_type = models.ForeignKey('MatchType', models.DO_NOTHING)
#     tier = models.ForeignKey('Tier', models.DO_NOTHING)

#     class Meta:
#         db_table = 'competition'


class CompetitionApplicantInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    applicantstatus = models.CharField(db_column='applicantStatus', max_length=4, blank=True, null=True)  # Field name made lowercase.
    applicantdate = models.DateTimeField(db_column='applicantDate', blank=True, null=True)  # Field name made lowercase.
    expireddate = models.DateTimeField(db_column='expiredDate', blank=True, null=True)  # Field name made lowercase.
    depositcheck = models.IntegerField(db_column='depositCheck', blank=True, null=True)  # Field name made lowercase.
    competition = models.ForeignKey(Competition, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'competition_applicant_info'


class CompetitionApplicantUser(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    competition_applicant = models.ForeignKey(CompetitionApplicantInfo, models.DO_NOTHING, db_column='Competition_applicant_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'competition_applicant_user'


class CompetitionPlayer(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    competition_player_info = models.ForeignKey('CompetitionPlayerInfo', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'competition_player'


class CompetitionPlayerInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    registrationdate = models.DateTimeField(db_column='registrationDate', blank=True, null=True)  # Field name made lowercase.
    competition = models.ForeignKey(Competition, models.DO_NOTHING)

    class Meta:
        managed = False  
        db_table = 'competition_player_info'


class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    gamenumber = models.IntegerField(db_column='gameNumber', blank=True, null=True)  # Field name made lowercase.
    scorea = models.IntegerField(db_column='scoreA', blank=True, null=True)  # Field name made lowercase.
    scoreb = models.IntegerField(db_column='scoreB', blank=True, null=True)  # Field name made lowercase.
    match = models.ForeignKey('Set', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'game'


# class ImageUrl(models.Model):
#     id = models.IntegerField(primary_key=True)
#     description = models.CharField(max_length=100, blank=True, null=True)
#     imageurl = models.TextField(db_column='imageUrl', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = False
#         db_table = 'image_url'


# class Match(models.Model):
#     id = models.IntegerField(primary_key=True)
#     matchround = models.IntegerField(db_column='matchRound', blank=True, null=True)  # Field name made lowercase.
#     matchnumber = models.IntegerField(db_column='matchNumber', blank=True, null=True)  # Field name made lowercase.
#     courtnumber = models.IntegerField(db_column='courtNumber', blank=True, null=True)  # Field name made lowercase.
#     competiton = models.ForeignKey(Competition, models.DO_NOTHING)
#     a_team = models.ForeignKey(CompetitionPlayerInfo, models.DO_NOTHING)
#     b_team = models.ForeignKey(CompetitionPlayerInfo, models.DO_NOTHING, related_name='match_b_team_set')

#     class Meta:
#         managed = False
#         db_table = 'match'


# class MatchType(models.Model):
#     id = models.IntegerField(primary_key=True)
#     gender = models.CharField(max_length=6, blank=True, null=True)
#     type = models.CharField(max_length=6, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'match_type'


# class Point(models.Model):
#     id = models.CharField(primary_key=True, max_length=255)
#     points = models.IntegerField(blank=True, null=True)
#     expireddate = models.DateTimeField(db_column='expiredDate', blank=True, null=True)
#     tier = models.ForeignKey('Tier', models.DO_NOTHING)
#     user = models.ForeignKey('Users', models.DO_NOTHING)
#     match_type = models.ForeignKey(MatchType, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'point'


# class Set(models.Model):
#     id = models.IntegerField(primary_key=True)
#     setnumber = models.IntegerField(db_column='setNumber', blank=True, null=True)  # Field name made lowercase.
#     scorea = models.IntegerField(db_column='scoreA', blank=True, null=True)  # Field name made lowercase.
#     scoreb = models.IntegerField(db_column='scoreB', blank=True, null=True)  # Field name made lowercase.
#     match_list = models.ForeignKey(Match, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'set'


# class Team(models.Model):
#     id = models.IntegerField(primary_key=True)
#     description = models.CharField(max_length=100, blank=True, null=True)
#     name = models.CharField(max_length=30, blank=True, null=True)
#     club = models.ForeignKey(Club, models.DO_NOTHING)
#     image_url = models.ForeignKey(ImageUrl, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'team'


# class Tier(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=6, blank=True, null=True)
#     level = models.IntegerField(blank=True, null=True)
#     match_type = models.ForeignKey(MatchType, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'tier'


# class Users(models.Model):
#     id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=30, blank=True, null=True)
#     phone = models.CharField(max_length=30, blank=True, null=True)
#     password = models.CharField(max_length=30, blank=True, null=True)
#     gender = models.CharField(max_length=6, blank=True, null=True)
#     birth = models.IntegerField(blank=True, null=True)
#     createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
#     updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
#     auth = models.CharField(max_length=6, blank=True, null=True)
#     club = models.ForeignKey(Club, models.DO_NOTHING)
#     team = models.ForeignKey(Team, models.DO_NOTHING)
#     image_url = models.ForeignKey(ImageUrl, models.DO_NOTHING)
#     tier = models.ForeignKey(Tier, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'users'


class UsersTiers(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    tier = models.ForeignKey(Tier, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_tiers'
