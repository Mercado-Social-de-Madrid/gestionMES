# Generated by Django 2.2.28 on 2022-11-15 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0036_auto_20221013_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='custom_fee',
            field=models.FloatField(blank=True, null=True, verbose_name='Cuota específica'),
        ),
        migrations.AddField(
            model_name='provider',
            name='payment_in_kind',
            field=models.BooleanField(default=False, verbose_name='Pago en especie'),
        ),
        migrations.AddField(
            model_name='provider',
            name='payment_in_kind_concept',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Concepto pago en especie'),
        ),
    ]
