# Generated by Django 5.0.4 on 2024-05-05 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0002_alter_club_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='club',
            name='image_url',
        ),
    ]
