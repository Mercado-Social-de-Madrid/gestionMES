# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-10-03 18:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comission',
            options={'permissions': (('mespermission_can_manage_commissions', 'Puede gestionar las comisiones'),), 'verbose_name': 'Comisi\xf3n', 'verbose_name_plural': 'Comisiones'},
        ),
    ]
