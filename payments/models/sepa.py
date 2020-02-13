# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _

from core.models import User
from payments.models import PendingPayment


class SepaBatch(models.Model):
    attempt = models.DateTimeField(auto_now_add=True, verbose_name=_('Añadido'))
    amount = models.FloatField(default=0, verbose_name=_('Cantidad total'))
    title = models.CharField(null=True, blank=True, verbose_name=_('Nombre'), max_length=180)
    generated_by = models.ForeignKey(User, null=True, verbose_name=_('Usuario que generó'), on_delete=models.SET_NULL)
    payments = models.ManyToManyField(PendingPayment, null=True, blank=True, verbose_name=_('Pagos incluídos'), related_name='sepa_batches')
    sepa_file = models.FileField(null=True, blank=True, upload_to='sepa', verbose_name=_('Fichero SEPA'))

    class Meta:
        verbose_name = _('Remesa SEPA')
        verbose_name_plural = _('Remesas SEPA')
        ordering = ['-generated_by']
        permissions = (
            ("mespermission_can_manage_sepa", _("Puede gestionar remesas de pagos SEPA")),
        )
