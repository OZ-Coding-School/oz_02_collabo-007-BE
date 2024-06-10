# Generated by Django 5.0.6 on 2024-06-07 14:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('match', '0003_match_created_at_match_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('set_number', models.IntegerField(blank=True, db_column='setNumber', null=True)),
                ('a_score', models.IntegerField(blank=True, db_column='Ascore', null=True)),
                ('b_score', models.IntegerField(blank=True, db_column='Bscore', null=True)),
                ('match_list', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='match.match')),
            ],
            options={
                'db_table': 'set',
            },
        ),
    ]