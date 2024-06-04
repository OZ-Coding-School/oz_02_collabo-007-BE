# Generated by Django 5.0.6 on 2024-06-03 18:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0017_competition_competition_type_and_more'),
        ('tier', '0004_remove_tier_level_alter_tier_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='tier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tier.tier'),
        ),
    ]