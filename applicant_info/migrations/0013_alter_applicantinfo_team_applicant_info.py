# Generated by Django 5.0.6 on 2024-06-14 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant_info', '0012_applicantinfo_team_applicant_game_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantinfo',
            name='team_applicant_info',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='applicant_list', to='applicant_info.teamapplicantinfo'),
        ),
    ]