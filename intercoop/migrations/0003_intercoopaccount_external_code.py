# Generated by Django 2.1.12 on 2019-12-17 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercoop', '0002_intercoopentity_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='intercoopaccount',
            name='external_code',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Identificador de socia externo'),
        ),
    ]
