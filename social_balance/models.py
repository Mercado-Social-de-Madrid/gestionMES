# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from accounts.models import Entity
from helpers import RandomFileName


class EntitySocialBalance(models.Model):

    entity = models.ForeignKey(Entity, null=False, blank=False, related_name='social_balances', verbose_name=_('Realizado por'), on_delete=models.CASCADE)
    is_exempt = models.BooleanField(default=False, verbose_name=_('Está exenta'))
    is_public = models.BooleanField(default=True, verbose_name=_('Informe público'))
    done = models.BooleanField(default=False, verbose_name=_('Realizado'))
    year = models.SmallIntegerField(default=2019, blank=False, null=False, verbose_name=_('Año'))
    external_id = models.CharField(null=True, blank=True, max_length=200, verbose_name=_('Identificador externo'))

    achievement = models.TextField(null=True, blank=True, verbose_name=_('Logro'))
    challenge = models.TextField(null=True, blank=True, verbose_name=_('Reto'))


    class Meta:
        verbose_name = _('Informe de balance social')
        verbose_name_plural = _('Informes de balance social')

    def __str__(self):
        return '{}: {}'.format(self.entity.cif, self.year)

    def __unicode__(self):
        return '{}: {}'.format(self.entity.cif, self.year)


class SocialBalanceBadge(models.Model):

    year = models.SmallIntegerField(default=2019, blank=False, null=False, verbose_name=_('Año'))
    layout_json = models.TextField(null=True, blank=True, verbose_name=_('JSON de configuración de layout'))
    base_img = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('balance/badges/'),
                        verbose_name='Plantilla para el sello de balance social',
                        processors=[ResizeToFit(1600, 1200, upscale=False)], format='PNG')