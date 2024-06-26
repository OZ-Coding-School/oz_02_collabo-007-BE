# Generated by Django 5.0.4 on 2024-05-01 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MatchType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('gender', models.CharField(blank=True, max_length=6, null=True)),
                ('type', models.CharField(blank=True, max_length=6, null=True)),
            ],
            options={
                'db_table': 'match_type',
            },
        ),
    ]
