# Generated by Django 2.1.12 on 2019-10-03 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simple_bpm', '0010_workflow_state_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process',
            name='member_type',
            field=models.CharField(blank=True, choices=[('consumidora', 'Socia consumidora'), ('colaboradora', 'Socia colaboradora'), ('proveedora', 'Socia proveedora')], max_length=30, null=True, verbose_name='Tipo de socia'),
        ),
        migrations.AlterField(
            model_name='processworkflowevent',
            name='completed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='processworkflowtask',
            name='completed_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
