# Generated by Django 5.0.6 on 2024-06-03 20:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('competition', '0017_competition_competition_type_and_more'),
        ('participant_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('matchround', models.IntegerField(blank=True, db_column='matchRound', null=True)),
                ('matchnumber', models.IntegerField(blank=True, db_column='matchNumber', null=True)),
                ('courtnumber', models.IntegerField(blank=True, db_column='courtNumber', null=True)),
                ('a_team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='participant_info.participantinfo')),
                ('b_team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='match_b_team_set', to='participant_info.participantinfo')),
                ('competiton', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='competition.competition')),
            ],
            options={
                'db_table': 'match',
            },
        ),
    ]