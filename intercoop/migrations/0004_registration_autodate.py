# Generated by Django 2.1.12 on 2019-12-17 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intercoop', '0003_intercoopaccount_external_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intercoopaccount',
            name='registration_date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Fecha de alta'),
        ),
    ]
