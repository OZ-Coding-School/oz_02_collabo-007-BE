# Generated by Django 5.0.6 on 2024-05-17 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0009_competition_max_participants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='max_participants',
            field=models.IntegerField(default=0),
        ),
    ]