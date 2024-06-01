# Generated by Django 5.0.6 on 2024-05-30 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('competition', '0016_remove_competition_deposit_refund_policy'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='competition_type',
            field=models.CharField(choices=[('tournament', '토너먼트'), ('league', '리그')], default='tournament', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='competition',
            name='bank_account_number',
            field=models.CharField(blank=True, db_column='bankAccountNumber', max_length=30, null=True),
        ),
    ]