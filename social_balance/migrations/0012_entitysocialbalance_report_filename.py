# Generated by Django 2.2.28 on 2022-12-05 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_balance', '0011_report_overwrite_storage'),
    ]

    operations = [
        migrations.AddField(
            model_name='entitysocialbalance',
            name='report_filename',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre archivo infografía'),
        ),
    ]
