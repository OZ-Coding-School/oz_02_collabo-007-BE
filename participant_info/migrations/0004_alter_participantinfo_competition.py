# Generated by Django 5.0.6 on 2024-06-08 23:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0019_merge_20240606_1539'),
        ('participant_info', '0003_participantinfo_applicant_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantinfo',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='competition.competition'),
        ),
    ]