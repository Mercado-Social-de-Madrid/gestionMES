# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import csv
import os

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from accounts.models import Entity
from helpers import RandomFileName
from helpers.csv import csv_value_to_boolean
from social_balance.renderer import BadgeRenderer

from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class EntitySocialBalance(models.Model):

    entity = models.ForeignKey(Entity, null=False, blank=False, related_name='social_balances', verbose_name=_('Realizado por'), on_delete=models.CASCADE)
    is_exempt = models.BooleanField(default=False, verbose_name=_('Está exenta'))
    is_public = models.BooleanField(default=True, verbose_name=_('Informe público'))
    done = models.BooleanField(default=False, verbose_name=_('Realizado'))
    year = models.SmallIntegerField(default=2019, blank=False, null=False, verbose_name=_('Año'))
    external_id = models.CharField(null=True, blank=True, max_length=200, verbose_name=_('Identificador externo'))

    achievement = models.TextField(null=True, blank=True, verbose_name=_('Logro'))
    challenge = models.TextField(null=True, blank=True, verbose_name=_('Reto'))

    badge_image = ProcessedImageField(null=True, blank=True, upload_to='balances', verbose_name=_('Imagen del sello'), format='PNG')
    report = models.FileField(null=True, blank=True, upload_to='reports', verbose_name=_('Informe'), storage=OverwriteStorage())

    class Meta:
        verbose_name = _('Informe de balance social')
        verbose_name_plural = _('Informes de balance social')
        permissions = (
            ("mespermission_can_view_social_balances", _("Puede gestionar los balances sociales")),
            ("mespermission_can_edit_social_balances", _("Puede editar los informes de balance social")),
        )


    def render_badge(self):
        badge = SocialBalanceBadge.objects.get(year=self.year)
        renderer = BadgeRenderer(badge)
        renderer.configure_webdriver()
        renderer.update_balance_image(self)

    @staticmethod
    def import_data(csv_file, year, delimiter=';'):

        results = []
        reader = csv.DictReader(codecs.iterdecode(csv_file, 'utf-8'), delimiter=delimiter)
        for row in reader:
            cif = row['cif']
            entity = Entity.objects.filter(cif=cif)
            if not entity.exists():

                results.append( "No se pudo encontrar entidad con CIF {}. ".format(cif))
                continue

            entity = entity.first()
            balance, created = EntitySocialBalance.objects.get_or_create(entity=entity, year=year)
            balance.done = csv_value_to_boolean(row['realizado'])
            balance.is_exempt = csv_value_to_boolean(row['exenta'])
            balance.is_public = csv_value_to_boolean(row['publico'])
            balance.achievement = row['logro']
            balance.challenge = row['reto']
            balance.save()

            results.append("Balance {} para {} actualizado. ".format(year, entity.name))

            if (year == settings.CURRENT_BALANCE_YEAR):
                if 'num_trab' in row:
                    entity.num_workers = int(row['num_trab'])
                if 'facturacion' in row:
                    aprox_income = int(row['facturacion'])
                    if (aprox_income > 1000):
                        # we can expect that they gave the total value
                        aprox_income = aprox_income / 1000
                    entity.aprox_income = aprox_income

                if 'num_trab' in row or 'facturacion' in row:
                    entity.save()

        return results

    def __str__(self):
        return '{}: {}'.format(self.entity.cif, self.year)

    def __unicode__(self):
        return '{}: {}'.format(self.entity.cif, self.year)


# @receiver(pre_save, sender=EntitySocialBalance)
# def set_report_filename(sender, instance, **kwargs):
#     if instance.report:
#         if not instance.entity.report_filename:
#             entity_name = instance.entity.name.replace(' ', '_')
#             instance.entity.report_filename = f'Mercado_Social_Madrid_Infografia_Balance_Social_{entity_name}.pdf'
#             instance.entity.save()
#
#         instance.report.name = instance.entity.report_filename


class SocialBalanceBadge(models.Model):

    year = models.SmallIntegerField(default=2019, blank=False, null=False, verbose_name=_('Año'))
    layout_json = models.TextField(null=True, blank=True, verbose_name=_('JSON de configuración de layout'))
    include_labels = models.BooleanField(default=False, verbose_name=_('Incluir etiqueta de Logro/Reto en el texto'))
    base_img = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('balance/badges/'),
                        verbose_name='Plantilla para el sello de balance social',
                        processors=[ResizeToFit(1600, 1200, upscale=False)], format='PNG')
    exempt_img = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('balance/badges/'),
                        verbose_name='Imagen de exenta',
                        processors=[ResizeToFit(900, 700, upscale=False)], format='PNG')
    undone_img = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('balance/badges/'),
                        verbose_name='Imagen de no realizada',
                        processors=[ResizeToFit(900, 700, upscale=False)], format='PNG')

    class Meta:
        verbose_name = _('Sello de balance social')
        verbose_name_plural = _('Sellos de balance social')
        permissions = (
            ("mespermission_can_view_social_badges", _("Puede ver las plantillas de sellos de balance social")),
            ("mespermission_can_create_social_badges", _("Puede crear plantillas de sellos de balance social")),
        )
