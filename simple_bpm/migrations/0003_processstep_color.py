# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-11-16 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_bpm', '0002_processstep_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='processstep',
            name='color',
            field=models.CharField(blank=True, default='#FFFFFF', max_length=20),
        ),
    ]
