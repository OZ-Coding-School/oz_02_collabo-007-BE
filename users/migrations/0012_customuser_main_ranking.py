# Generated by Django 5.0.6 on 2024-06-13 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_merge_20240606_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='main_ranking',
            field=models.BooleanField(default=False),
        ),
    ]