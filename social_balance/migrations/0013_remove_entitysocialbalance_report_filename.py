# Generated by Django 2.2.28 on 2022-12-07 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_balance', '0012_entitysocialbalance_report_filename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entitysocialbalance',
            name='report_filename',
        ),
    ]
