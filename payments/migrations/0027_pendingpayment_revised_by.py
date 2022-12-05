# Generated by Django 2.2.28 on 2022-10-11 16:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0026_pendingpayment_invoice_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pendingpayment',
            name='revised_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario que revisó'),
        ),
    ]