# Generated by Django 5.0.6 on 2024-06-07 21:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0003_alter_participant_participant_info'),
        ('participant_info', '0002_remove_participantinfo_registered_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='participant_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='participant_info.participantinfo'),
        ),
    ]