# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _


class LegalForm(models.Model):

    title = models.CharField(null=False, max_length=250,  verbose_name=_('Nombre'))
    class Meta:
        verbose_name = _('Forma legal')
        verbose_name_plural = _('Formas legales')

    def __unicode__(self):
        return self.title if self.title else ''