# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _


class SocialCapital(models.Model):

    amount = models.FloatField(null=True, blank=True, verbose_name=_('Capital social'), default=0)

    paid = models.BooleanField(default=False, verbose_name=_('Pagado'))
    paid_timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha pago'))
    paid_type = models.CharField(null=True, blank=True, max_length=30, verbose_name=_('Modo de pago'))

    returned = models.BooleanField(default=False, verbose_name=_('Devuelto'))
    returned_timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha de devolución'))

    class Meta:
        verbose_name = _('Capital social')
        verbose_name_plural = _('Capitales sociales')
        permissions = (
            ("mespermission_can_view_social_capital", _("Puede ver los capitales sociales")),
        )
