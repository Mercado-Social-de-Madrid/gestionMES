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

    badge_image = ProcessedImageField(null=True, blank=True, upload_to='balances', verbose_name=_('Imagen del sello'), format='PNG')
    report = models.FileField(null=True, blank=True, upload_to='reports', verbose_name=_('Informe'))

    class Meta:
        verbose_name = _('Informe de balance social')
        verbose_name_plural = _('Informes de balance social')
        permissions = (
            ("mespermission_can_view_social_balances", _("Puede gestionar los balances sociales")),
            ("mespermission_can_edit_social_balances", _("Puede editar los informes de balance social")),
        )

    def __str__(self):
        return '{}: {}'.format(self.entity.cif, self.year)

    def __unicode__(self):
        return '{}: {}'.format(self.entity.cif, self.year)



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
