# Generated by Django 5.0.6 on 2024-06-08 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0006_alter_match_a_team_alter_match_b_team_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='courtnumber',
            new_name='court_number',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='matchnumber',
            new_name='match_number',
        ),
        migrations.RenameField(
            model_name='match',
            old_name='matchround',
            new_name='match_round',
        ),
    ]