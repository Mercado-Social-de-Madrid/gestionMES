# Generated by Django 2.1.12 on 2021-03-09 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercoop', '0007_view_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='intercoopaccount',
            name='referral_source',
            field=models.TextField(blank=True, null=True, verbose_name='Cómo nos has conocido?'),
        ),
    ]
