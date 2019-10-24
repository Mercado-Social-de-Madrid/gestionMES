# Generated by Django 2.1.12 on 2019-10-24 14:13

from django.db import migrations, models
import helpers.filesystem
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('social_balance', '0005_entitysocialbalance_badge_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialbalancebadge',
            name='exempt_img',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=helpers.filesystem.RandomFileName('balance/badges/'), verbose_name='Imagen de exenta'),
        ),
        migrations.AddField(
            model_name='socialbalancebadge',
            name='include_labels',
            field=models.BooleanField(default=False, verbose_name='Incluir etiqueta de Logro/Reto en el texto'),
        ),
        migrations.AddField(
            model_name='socialbalancebadge',
            name='undone_img',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=helpers.filesystem.RandomFileName('balance/badges/'), verbose_name='Imagen de no realizada'),
        ),
    ]
