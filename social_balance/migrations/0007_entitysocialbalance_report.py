# Generated by Django 2.1.12 on 2019-10-30 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_balance', '0006_auto_20191024_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='entitysocialbalance',
            name='report',
            field=models.FileField(blank=True, null=True, upload_to='reports', verbose_name='Informe'),
        ),
    ]
