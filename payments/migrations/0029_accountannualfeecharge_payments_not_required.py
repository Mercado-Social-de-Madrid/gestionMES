# Generated by Django 2.2.28 on 2022-12-22 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0028_pendingpayment_is_social_capital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountannualfeecharge',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fee_charges', to='payments.PendingPayment'),
        ),
        migrations.AlterField(
            model_name='accountannualfeecharge',
            name='payments',
            field=models.ManyToManyField(blank=True, null=True, related_name='fee_split_charges', to='payments.PendingPayment'),
        ),
    ]
