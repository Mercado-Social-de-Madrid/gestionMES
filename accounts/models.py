# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext as _
from imagekit import ImageSpec, register
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit, ResizeToFill
from polymorphic.models import PolymorphicModel

from helpers import RandomFileName
from mes import settings

TERR_LOCAL = 'local'
TERR_COUNTRY = 'estatal'
TERRITORY_OPTIONS = (
    (TERR_LOCAL, 'Local'),
    (TERR_COUNTRY, 'Estatal'),
)

ACTIVE = 'activa'
INITIAL_PAYMENT = 'pagoinicial'
PENDING_PAYMENT = 'pagopendiente'
OPTED_OUT = 'baja'
CANCELED = 'anulada'
SIGNUP = 'acogida'

ACCOUNT_STATUSES = (
    (ACTIVE, 'Activa'),
    (SIGNUP, 'En proceso de acogida'),
    (INITIAL_PAYMENT, 'Pendiente de pago inicial'),
    (PENDING_PAYMENT, 'Pago de cuota pendiente'),
    (CANCELED, 'Anulada por impago'),
    (OPTED_OUT, 'Baja'),
)

class LegalForm(models.Model):

    title = models.CharField(null=False, max_length=250,  verbose_name=_('Nombre'))
    class Meta:
        verbose_name = _('Forma legal')
        verbose_name_plural = _('Formas legales')

class Category(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=True, blank=True, verbose_name='Nombre', max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    color = models.CharField(null=True, blank=True, verbose_name='Color de etiqueta (código hexadecimal)', max_length=30)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __unicode__(self):
        return self.name if self.name else ''


class MaxResize(ImageSpec):
    processors = [ResizeToFit(1024, 1024)]
    format = 'JPEG'
    options = {'quality': 80}

register.generator('mes:profile:max_resize', MaxResize)


class Account(PolymorphicModel):

    status = models.CharField(null=False, default=ACTIVE, max_length=20, choices=ACCOUNT_STATUSES, verbose_name=_('Estado'))
    cif = models.CharField(max_length=30, null=False, blank=False, verbose_name=_('NIF/CIF'), unique=True)
    legal_form = models.ForeignKey(LegalForm, null=True, verbose_name=_('Forma legal'))
    contact_phone = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Teléfono de contacto'))
    contact_email = models.EmailField(null=False, verbose_name=_('Email de contacto'))
    member_type = models.CharField(null=True, blank=True, max_length=30, choices=settings.MEMBER_TYPES, verbose_name=_('Tipo de socia'))
    address = models.TextField(null=True, blank=True, verbose_name=_('Dirección'))
    city = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Municipio'))
    province = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Provincia'))
    postalcode = models.CharField(null=True, blank=True, max_length=10, verbose_name=_('Código Postal'))
    iban_code = models.CharField(null=True, blank=True, max_length=50, verbose_name=_('Cuenta bancaria (IBAN)'))
    registration_date = models.DateField(verbose_name=_('Fecha de alta'))
    cr_member = models.BooleanField(default=False, verbose_name=_('Miembro Consejo Rector'))

    class Meta:
        verbose_name = _('Socia')
        verbose_name_plural = _('Socias')
        permissions = (
            ("mespermission_can_view_accounts", _("Puede ver la lista de socias")),
        )

    def __str__(self):
        return "{}".format(self.group.name).encode('utf-8')


class Consumer(Account):
    first_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Nombre'))
    last_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Apellidos'))


class Entity(Account):
    categories = models.ManyToManyField(Category, blank=True, verbose_name='Categorías', related_name='entities')
    territory = models.CharField(null=False, default=TERR_LOCAL, max_length=20, choices=TERRITORY_OPTIONS,
                                 verbose_name=_('Ámbito'))
    assisted_last_fair = models.BooleanField(default=False, verbose_name=_('Asistió a la última feria'))
    latitude = models.FloatField(null=False, verbose_name='Latitud', default=0)
    longitude = models.FloatField(null=False, verbose_name='Longitud', default=0)

    logo = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('entities/'),
                               verbose_name='Logo en alta resolución',
                               processors=[ResizeToFit(1024, 1024, upscale=False)], format='JPEG', options={'quality': 80})

    banner = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('entities/'),
                               verbose_name='Banner alta resolución',
                               processors=[ResizeToFit(1024, 1024, upscale=False)], format='JPEG', options={'quality': 80})

    start_year = models.PositiveSmallIntegerField(blank=True, null=True, default=datetime.now,
                                validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
                                verbose_name=_('Año de inicio del proyecto'))
    contact_person = models.TextField(null=True, blank=True, verbose_name=_('Persona de contacto'))


class Colaborator(Entity):
    collaboration = models.TextField(blank=True, verbose_name=_('Modo de colaboración'))

class Provider(Entity):
    is_physical_store = models.BooleanField(default=False, verbose_name=_('Es tienda física'))
    num_workers = models.IntegerField(default=1, verbose_name=_('Número de trabajadoras'))
    aprox_income = models.IntegerField(default=0, verbose_name=_('Facturación último año'))

