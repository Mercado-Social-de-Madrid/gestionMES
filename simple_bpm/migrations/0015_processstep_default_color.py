# Generated by Django 2.2.28 on 2022-11-29 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_bpm', '0014_event_no_autotime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processstep',
            name='color',
            field=models.CharField(blank=True, default='#653776', max_length=20),
        ),
    ]
