# Generated by Django 2.2.28 on 2022-11-21 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0027_pendingpayment_revised_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingpayment',
            name='is_social_capital',
            field=models.BooleanField(default=False, verbose_name='Es Capital Social'),
        ),
    ]
