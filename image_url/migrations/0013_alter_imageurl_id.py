# Generated by Django 5.0.6 on 2024-05-12 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_url', '0012_alter_imageurl_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageurl',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
