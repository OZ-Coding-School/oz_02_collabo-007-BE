# Generated by Django 5.0.6 on 2024-05-26 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicant_info', '0005_alter_applicantinfo_competition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicantinfo',
            name='is_waiting',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]