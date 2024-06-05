# Generated by Django 5.0.6 on 2024-06-05 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0001_initial'),
        ('participant_info', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='applicant_info',
        ),
        migrations.AddField(
            model_name='participant',
            name='participant_info',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='participant_info.participantinfo'),
            preserve_default=False,
        ),
    ]
