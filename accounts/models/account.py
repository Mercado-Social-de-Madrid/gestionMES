# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext as _
from django.utils.timezone import now

from imagekit import ImageSpec, register
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel

from accounts.models import Category, LegalForm
from accounts.models.collaboration import Collaboration

from helpers import RandomFileName

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



class MaxResize(ImageSpec):
    processors = [ResizeToFit(1024, 1024)]
    format = 'JPEG'
    options = {'quality': 80}

register.generator('mes:profile:max_resize', MaxResize)



class AccountsManager(PolymorphicManager):

    def active(self):
        qs = self.get_queryset()
        return qs.filter( Q(status=ACTIVE) | Q(status=INITIAL_PAYMENT) | Q(status=PENDING_PAYMENT) )


class Account(PolymorphicModel):

    status = models.CharField(null=False, default=ACTIVE, max_length=20, choices=ACCOUNT_STATUSES, verbose_name=_('Estado'))
    cif = models.CharField(max_length=30, null=False, blank=False, verbose_name=_('NIF/CIF'), unique=True)
    legal_form = models.ForeignKey(LegalForm, null=True, verbose_name=_('Forma legal'), on_delete=models.SET_NULL)
    contact_phone = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Teléfono de contacto'))
    contact_email = models.EmailField(null=False, verbose_name=_('Email de contacto'))
    member_type = models.CharField(null=True, blank=True, max_length=30, choices=settings.MEMBER_TYPES, verbose_name=_('Tipo de socia'))
    address = models.TextField(null=True, blank=True, verbose_name=_('Dirección'))
    city = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Municipio'))
    province = models.CharField(null=True, blank=True, max_length=100, verbose_name=_('Provincia'))
    postalcode = models.CharField(null=True, blank=True, max_length=10, verbose_name=_('Código Postal'))
    iban_code = models.CharField(null=True, blank=True, max_length=50, verbose_name=_('Cuenta bancaria (IBAN)'))

    cr_member = models.BooleanField(default=False, verbose_name=_('Miembro Consejo Rector'))
    pay_by_debit = models.BooleanField(default=False, verbose_name=_('Domiciliar la cuota'),
                                       help_text=_(
                                           'Permito que el MES domicilie en mi cuenta bancaria mi cuota anual y el capital social'))

    cyclos_user = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Antiguo usuario en Cyclos'))

    last_updated = models.DateTimeField(verbose_name=_('Última actualización'), null=True, blank=True)
    registration_date = models.DateField(verbose_name=_('Fecha de alta'), null=True, blank=True)
    opted_out_date = models.DateField(verbose_name=_('Fecha de baja'), null=True, blank=True)

    # Custom model manager
    objects = AccountsManager()

    class Meta:
        verbose_name = _('Socia')
        verbose_name_plural = _('Socias')
        permissions = (
            ("mespermission_can_view_accounts", _("Puede ver la lista de socias")),
            ("mespermission_can_view_reports", _("Puede ver los informes de socias")),
        )

    @property
    def template_prefix(self):
        return 'account'

    @property
    def detail_url(self):
        return 'accounts:provider_detail'

    @property
    def display_name(self):
        return self.cif

    @property
    def invoice_name(self):
        return self.cif

    @property
    def is_active(self):
        return self.status == ACTIVE or self.status == INITIAL_PAYMENT or self.status == PENDING_PAYMENT

    @property
    def registered_in_app(self):
        return self.app_user.exists() and self.app_user.first().username is not None

    @property
    def current_fee(self):
        return None # there is no general fee defined for all the account types

    def __str__(self):
        return self.display_name


class Consumer(Account):
    first_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Nombre'))
    last_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Apellidos'))

    class Meta:
        verbose_name = _('Consumidora')
        verbose_name_plural = _('Consumidoras')

    @property
    def template_prefix(self):
        return 'consumer'

    @property
    def detail_url(self):
        return 'accounts:consumer_detail'

    @property
    def display_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def current_fee(self):
        from payments.models import FeeRange
        return FeeRange.DEFAULT_CONSUMER_FEE


class Entity(Account):
    name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Nombre'))
    business_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Razón social'))
    categories = models.ManyToManyField(Category, verbose_name='Categorías', related_name='entities')
    territory = models.CharField(null=False, default=TERR_LOCAL, max_length=20, choices=TERRITORY_OPTIONS, verbose_name=_('Ámbito'))
    contact_phone2 = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Teléfono de contacto (2)'))
    contact_email2 = models.EmailField(null=True, blank=True, verbose_name=_('Email de contacto (2)'))

    assisted_last_fair = models.BooleanField(default=False, verbose_name=_('Asistió a la última feria'))
    latitude = models.FloatField(null=False, verbose_name='Latitud', default=settings.INITIAL_LATITUDE)
    longitude = models.FloatField(null=False, verbose_name='Longitud', default=settings.INITIAL_LONGITUDE)
    public_address = models.TextField(null=True, blank=True, verbose_name=_('Dirección pública'), help_text='Dirección que aparece en el perfil de la entidad en la app del MES')
    logo = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('entities/'),
                               verbose_name='Logo en alta resolución',
                               processors=[ResizeToFit(1024, 1024, upscale=False)], format='JPEG', options={'quality': 80})

    banner = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('entities/'),
                               verbose_name='Banner alta resolución',
                               processors=[ResizeToFit(1024, 1024, upscale=False)], format='JPEG', options={'quality': 80})

    start_year = models.PositiveSmallIntegerField(blank=True, null=True, default=datetime.now().year,
                                validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
                                verbose_name=_('Año de inicio del proyecto'))
    contact_person = models.TextField(null=True, blank=True, verbose_name=_('Persona de contacto'))

    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    short_description = models.TextField(null=True, blank=True, verbose_name='Descripción corta')

    bonus_percent_entity = models.FloatField(default=0, verbose_name='Porcentaje de bonificación a entidades',
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    bonus_percent_general = models.FloatField(default=0, verbose_name='Porcentaje de bonificación general',
                                              validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_percent_payment = models.FloatField(default=0, verbose_name='Máximo porcentaje de pago aceptado',
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    payment_conditions = models.TextField(null=True, blank=True, verbose_name=_('Condiciones uso Etics'))

    # Social links
    facebook_link = models.CharField(null=True, blank=True, verbose_name='Página de Facebook', max_length=250)
    webpage_link = models.CharField(null=True, blank=True, verbose_name='Página web', max_length=250)
    twitter_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Twitter', max_length=250)
    telegram_link = models.CharField(null=True, blank=True, verbose_name='Canal de Telegram', max_length=250)
    instagram_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Instagram', max_length=250)

    num_workers_male_partners = models.IntegerField(null=True, blank=True, verbose_name=_('Núm. hombres socios trabajadores'))
    num_workers_female_partners = models.IntegerField(null=True, blank=True,
                                                    verbose_name=_('Núm. mujeres socias trabajadoras'))
    num_workers_male_non_partners = models.IntegerField(null=True, blank=True,
                                                    verbose_name=_('Núm. hombres no socios trabajadores'))
    num_workers_female_non_partners = models.IntegerField(null=True, blank=True,
                                                    verbose_name=_('Núm. mujeres no socias trabajadoras'))

    highest_salary = models.FloatField(null=True, blank=True, verbose_name=_('Salario bruto anual más alto'))
    lowest_salary = models.FloatField(null=True, blank=True, verbose_name=_('Salario bruto anual más bajo'))
    benefits_destination = models.TextField(blank=True, verbose_name=_('A qué se destinan los beneficios de la entidad (si los hay)'))
    apportations = models.TextField(blank=True, verbose_name=_('Qué trata de aportar vuestro proyecto a la transformación social'))
    networking = models.TextField(blank=True, verbose_name=_('Redes/organizaciones/iniciativas de transformación social de las que la entidad forma parte'))

    hidden_in_catalog = models.BooleanField(default=False, verbose_name=_('Oculta en el catálogo'), help_text='No mostrar esta entidad en el catálogo de la web')

    collabs = models.ManyToManyField(Collaboration, verbose_name=_('Colaboraciones'), related_name='entities', through='EntityCollaboration')

    class Meta:
        verbose_name = _('Entidad')
        verbose_name_plural = _('Entidades')
        ordering = ['name']

    @property
    def template_prefix(self):
        return 'entity'

    @property
    def display_name(self):
        return self.name

    @property
    def invoice_name(self):
        return self.business_name

    @property
    def detail_url(self):
        return 'accounts:entity_detail'

    @property
    def category_list(self):
        return ";".join([cat.name for cat in self.categories.all()])

    def get_active_collaborations(self):
        return EntityCollaboration.objects.filter(entity=self, ended__isnull=True)

class Colaborator(Entity):
    is_sponsor = models.BooleanField(default=False, verbose_name=_('Es patrocinadora'))
    is_collaborator = models.BooleanField(default=False, verbose_name=_('Es colaboradora'))
    collaboration = models.TextField(blank=True, verbose_name=_('Modo de colaboración'))
    special_agreement = models.TextField(blank=True, verbose_name=_('Acuerdos especiales'))
    custom_fee = models.FloatField(null=True, blank=True, verbose_name=_('Cuota específica'))

    class Meta:
        verbose_name = _('Entidad especial')
        verbose_name_plural = _('Entidades especiales')
        ordering = ['name']

    @property
    def detail_url(self):
        return 'accounts:entity_detail'

    @property
    def current_fee(self):
        from payments.models import FeeRange
        return self.custom_fee if (self.custom_fee and self.custom_fee > 0) else FeeRange.DEFAULT_SPECIAL_FEE


class Provider(Entity):
    is_physical_store = models.BooleanField(default=False, verbose_name=_('Es tienda física'))
    num_workers = models.IntegerField(default=1, verbose_name=_('Número de trabajadoras'))
    aprox_income = models.IntegerField(default=0, verbose_name=_('Facturación último año'))

    class Meta:
        verbose_name = _('Proveedora')
        verbose_name_plural = _('Proveedoras')

    @property
    def detail_url(self):
        return 'accounts:provider_detail'

    @property
    def template_prefix(self):
        return 'provider'

    @property
    def current_fee(self):
        from payments.models import FeeRange
        return FeeRange.calculate_provider_fee(self)

    @property
    def has_logo(self):
        return bool(self.logo)


class EntityCollaboration(models.Model):
    entity = models.ForeignKey(Entity, related_name='entity_colabs', verbose_name=_('Entidad'), on_delete=models.CASCADE, null=True)
    order = models.IntegerField(verbose_name=_('Orden'), null=True, blank=True)
    collaboration = models.ForeignKey(Collaboration, verbose_name=_('Modo de colaboración'), related_name='entities_collab', on_delete=models.SET_NULL, null=True, blank=True)
    special_agreement = models.TextField(blank=True, verbose_name=_('Acuerdos especiales'))
    custom_fee = models.FloatField(null=True, blank=True, verbose_name=_('Cuota específica'), help_text=_('Cuota anual. Si se deja este campo vacío, se utilizará la cuota por defecto definida en el modo de colaboración'))
    started =  models.DateField(verbose_name=_('Inicio de la colaboración'), default=now)
    ended =  models.DateField(verbose_name=_('Fin de la colaboración'), null=True, blank=True)

    class Meta:
        verbose_name = _('Colaboración de entidad')
        verbose_name_plural = _('Colaboraciones con entidad')
        ordering = ['-started']
