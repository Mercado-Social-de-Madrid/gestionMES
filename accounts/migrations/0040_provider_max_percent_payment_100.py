# Generated by Django 2.2.28 on 2022-11-28 09:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_socialcapital_paid_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='max_percent_payment',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Máximo porcentaje de pago aceptado'),
        ),
    ]
