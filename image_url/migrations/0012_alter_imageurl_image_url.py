# Generated by Django 5.0.6 on 2024-05-12 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_url', '0011_alter_imageurl_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageurl',
            name='image_url',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]