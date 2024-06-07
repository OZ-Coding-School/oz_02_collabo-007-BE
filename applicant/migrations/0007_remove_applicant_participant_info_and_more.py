# Generated by Django 5.0.6 on 2024-06-04 23:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant', '0006_remove_applicant_applicant_info_and_more'),
        ('applicant_info', '0010_alter_applicantinfo_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='participant_info',
        ),
        migrations.AddField(
            model_name='applicant',
            name='applicant_info',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='applicant_info.applicantinfo'),
            preserve_default=False,
        ),
    ]
