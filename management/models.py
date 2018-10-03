# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import gettext as _

class Comission(models.Model):

    group = models.OneToOneField(Group, unique=True)
    label_color = models.CharField(max_length=20, blank=True, default="#FFFFFF")

    class Meta:
        verbose_name = _('Comisión')
        verbose_name_plural = _('Comisiones')

    def __str__(self):
        return "{}".format(self.group.name)