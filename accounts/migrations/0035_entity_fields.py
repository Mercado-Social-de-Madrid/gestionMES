# Generated by Django 2.2.28 on 2022-10-11 16:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0034_account_cif'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='latitude',
            field=models.FloatField(default=1.0, verbose_name='Latitud'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='longitude',
            field=models.FloatField(default=1.0, verbose_name='Longitud'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='max_percent_payment',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Máximo porcentaje de pago aceptado'),
        ),
        migrations.AlterField(
            model_name='entity',
            name='start_year',
            field=models.PositiveSmallIntegerField(blank=True, default=2022, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2022)], verbose_name='Año de inicio del proyecto'),
        ),
    ]