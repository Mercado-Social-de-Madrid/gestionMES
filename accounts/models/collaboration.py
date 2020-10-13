# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models
from django.utils.translation import gettext as _



class Collaboration(models.Model):

    name = models.CharField(null=True, blank=True, verbose_name='Tipo', max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    color = models.CharField(null=True, blank=True, verbose_name='Color de etiqueta (código hexadecimal)', max_length=30)
    default_fee = models.FloatField(null=True, blank=True, verbose_name=_('Cuota por defecto'))

    class Meta:
        verbose_name = _('Tipos de colaboración')
        verbose_name_plural = _('Tipos de colaboración')
        ordering = ['name']


    def __str__(self):
        return self.name if self.name else ''