# Generated by Django 2.1.12 on 2020-06-16 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_balance', '0009_balanceprocess'),
    ]

    operations = [
        migrations.AddField(
            model_name='balanceprocess',
            name='balance_type',
            field=models.CharField(blank=True, choices=[('BSacotado', 'Acotado'), ('BSlargo', 'Largo'), ('BSexenta', 'Exenta')], max_length=30, null=True, verbose_name='Tipo de balance'),
        ),
    ]
