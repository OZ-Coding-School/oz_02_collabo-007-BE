# Generated by Django 5.0.6 on 2024-05-12 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchtype', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchtype',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
