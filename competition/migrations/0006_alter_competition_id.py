# Generated by Django 5.0.6 on 2024-05-13 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0005_competition_created_at_competition_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
