# Generated by Django 2.1.12 on 2020-06-03 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_account_lastupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupprocess',
            name='reference',
            field=models.TextField(blank=True, null=True, verbose_name='Cómo nos conocisste'),
        ),
    ]
