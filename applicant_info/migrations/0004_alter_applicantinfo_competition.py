# Generated by Django 5.0.6 on 2024-05-20 23:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant_info', '0003_alter_applicantinfo_status'),
        ('competition', '0011_competition_deposit_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantinfo',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='competition.competition'),
        ),
    ]