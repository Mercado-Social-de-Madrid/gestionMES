# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from datetime import datetime

import dateutil
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit

from accounts.models import Account, Provider, Consumer
from currency.exceptions import AllInvitesSent
from currency_server import create_account
from helpers import send_template_email, RandomFileName
from simple_bpm.models import ProcessWorkflow, CurrentProcess, CurrentProcessStep, ProcessWorkflowEvent

INVITE_DURATION_YEARS = 3

class IntercoopEntity(models.Model):

    name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Nombre'))
    expiration = models.IntegerField(default=INVITE_DURATION_YEARS, verbose_name=_('Años de validez'))
    include_code = models.BooleanField(default=True, verbose_name=_('Incluir identificador de socia externa para validación'))
    code_label = models.CharField(null=True, blank=True, max_length=200, verbose_name=_('Etiqueta del identificador'))

    logo = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('intercoop/'),
                               verbose_name='Logo en alta resolución',
                               processors=[ResizeToFit(1024, 1024, upscale=False)], format='JPEG',
                               options={'quality': 80})

    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    slug = models.CharField(null=True, blank=True, max_length=200,verbose_name='Enlace permanente', help_text='Identificador para el enlace de alta')

    class Meta:
        verbose_name = _('Entidad de intercooperación')
        verbose_name_plural = _('Entidades de intercooperación')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name



class IntercoopAccount(models.Model):

    entity = models.ForeignKey(IntercoopEntity, null=False, verbose_name=_('Entidad asociada'), related_name='accounts', on_delete=models.CASCADE)
    active = models.BooleanField(default=True, verbose_name=_('Activa'))
    cif = models.CharField(null=False,max_length=30, verbose_name=_('NIF/CIF'), unique=True)
    first_name = models.CharField(null=False,max_length=250, verbose_name=_('Nombre'))
    last_name = models.CharField(null=False,max_length=250, verbose_name=_('Apellidos'))

    contact_phone = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Teléfono de contacto'))
    contact_email = models.EmailField(null=False, verbose_name=_('Email de contacto'))
    address = models.TextField(null=True, blank=True, verbose_name=_('Dirección'))
    city = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Municipio'))
    province = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Provincia'))
    postalcode = models.CharField(null=True, blank=True, max_length=10, verbose_name=_('Código Postal'))

    registration_date = models.DateField(verbose_name=_('Fecha de alta'), null=True, blank=True, auto_now_add=True)

    external_code = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Identificador de socia externo'))
    validated = models.BooleanField(default=False, verbose_name=_('Validada'))
    newsletter_check = models.BooleanField(default=False, verbose_name=_('Acepta alta en listas de correo'))

    class Meta:
        verbose_name = _('Socia intercooperación')
        verbose_name_plural = _('Socias intercooperación')

    @property
    def template_prefix(self):
        return 'intercoop'

    @property
    def display_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def is_active(self):
        return self.active

    def __str__(self):
        return self.display_name
