# Generated by Django 5.0.6 on 2024-05-29 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club_applicant', '0003_alter_clubapplicant_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubapplicant',
            name='status',
            field=models.CharField(choices=[('pending', '대기'), ('approved', '승인'), ('rejected', '거절')], default='pending', max_length=255),
        ),
    ]