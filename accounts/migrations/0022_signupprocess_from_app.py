# Generated by Django 2.1.12 on 2019-10-14 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_signupprocess_newsletter_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='signupprocess',
            name='from_app',
            field=models.BooleanField(default=False, verbose_name='Registro desde la app'),
        ),
    ]
