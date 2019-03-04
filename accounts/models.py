# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from imagekit import ImageSpec, register
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit, ResizeToFill
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel

from helpers import RandomFileName
from django.conf import settings
from simple_bpm.models import ProcessWorkflow, CurrentProcess, CurrentProcessStep, ProcessWorkflowEvent

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

STEP_SIGNUP_FORM = 'signup_form'
STEP_CONSUMER_FORM = 'consumer_form'
STEP_PAYMENT_RULES = 'payment_rules'
STEP_PAYMENT = 'payment'
STEP_CONSUMER_PAYMENT = 'consumer_payment'

class LegalForm(models.Model):

    title = models.CharField(null=False, max_length=250,  verbose_name=_('Nombre'))
    class Meta:
        verbose_name = _('Forma legal')
        verbose_name_plural = _('Formas legales')

    def __unicode__(self):
        return self.title if self.title else ''

class Category(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=True, blank=True, verbose_name='Nombre', max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    color = models.CharField(null=True, blank=True, verbose_name='Color de etiqueta (código hexadecimal)', max_length=30)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
        permissions = (
            ("mespermission_can_manage_categories", _("Puede gestionar las categorías")),
        )

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
    registration_date = models.DateField(verbose_name=_('Fecha de alta'), null=True, blank=True)
    cr_member = models.BooleanField(default=False, verbose_name=_('Miembro Consejo Rector'))
    pay_by_debit = models.BooleanField(default=False, verbose_name=_('Domiciliar la cuota'),
                                       help_text=_(
                                           'Permito que el MES domicilie en mi cuenta bancaria mi cuota anual y el capital social'))

    cyclos_user = models.CharField(null=True, blank=True, max_length=150, verbose_name=_('Antiguo usuario en Cyclos'))

    class Meta:
        verbose_name = _('Socia')
        verbose_name_plural = _('Socias')
        permissions = (
            ("mespermission_can_view_accounts", _("Puede ver la lista de socias")),
        )

    @property
    def template_prefix(self):
        return 'account'

    @property
    def display_name(self):
        return self.cif

    def __str__(self):
        return self.display_name.encode('utf-8')


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
    def display_name(self):
        return "{} {}".format(self.first_name, self.last_name)



class Entity(Account):
    name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Nombre'))
    business_name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Razón social'))
    categories = models.ManyToManyField(Category, verbose_name='Categorías', related_name='entities')
    territory = models.CharField(null=False, default=TERR_LOCAL, max_length=20, choices=TERRITORY_OPTIONS,
                                 verbose_name=_('Ámbito'))
    assisted_last_fair = models.BooleanField(default=False, verbose_name=_('Asistió a la última feria'))
    latitude = models.FloatField(null=False, verbose_name='Latitud', default=settings.INITIAL_LATITUDE)
    longitude = models.FloatField(null=False, verbose_name='Longitud', default=settings.INITIAL_LONGITUDE)

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

    class Meta:
        verbose_name = _('Entidad')
        verbose_name_plural = _('Entidades')
        ordering = ['name']

    @property
    def display_name(self):
        return self.name


class Colaborator(Entity):
    collaboration = models.TextField(blank=True, verbose_name=_('Modo de colaboración'))


class Provider(Entity):
    is_physical_store = models.BooleanField(default=False, verbose_name=_('Es tienda física'))
    num_workers = models.IntegerField(default=1, verbose_name=_('Número de trabajadoras'))
    aprox_income = models.IntegerField(default=0, verbose_name=_('Facturación último año'))

    class Meta:
        verbose_name = _('Proveedora')
        verbose_name_plural = _('Proveedoras')

    @property
    def template_prefix(self):
        return 'provider'


class SignupsManager(models.Manager):

    def pending(query, entity=None):
        return query.filter(workflow__completed=False)

    def create_process(self, account):
        signup = self.create(account=account)

        account.status = SIGNUP
        account.save()

        if account.get_real_instance_class() is Provider:
            signup.name = account.name
            signup.contact_phone = account.contact_phone
            signup.contact_email = account.contact_email
            signup.contact_person = account.contact_person
            signup.member_type = settings.MEMBER_PROV

            process = CurrentProcess.objects.filter(shortname='prov_signup').first().process
            step = CurrentProcessStep.objects.filter(process=process, shortname=STEP_SIGNUP_FORM).first().process_step

            workflow = ProcessWorkflow()
            workflow.process = process
            workflow.current_state = step
            workflow.save()
            signup.workflow = workflow
            signup.save()

            workflow.add_comment(user=None, comment='La entidad completa el formulario')


        if account.get_real_instance_class() is Consumer:
            signup.name = account.display_name
            signup.contact_phone = account.contact_phone
            signup.contact_email = account.contact_email
            signup.contact_person = account.display_name
            signup.member_type = settings.MEMBER_CONSUMER

            process = CurrentProcess.objects.filter(shortname='cons_signup').first().process
            step = CurrentProcessStep.objects.filter(process=process, shortname=STEP_CONSUMER_FORM).first().process_step

            workflow = ProcessWorkflow()
            workflow.process = process
            workflow.current_state = step
            workflow.save()
            signup.workflow = workflow
            signup.save()

            workflow.add_comment(user=None, comment='La consumidora completa el formulario')



class SignupProcess(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, auto_created=True, verbose_name=_('Identificador proceso'))
    workflow = models.ForeignKey(ProcessWorkflow, null=True, verbose_name=_('Seguimiento del proceso'))
    member_type = models.CharField(null=True, blank=True, max_length=30, choices=settings.MEMBER_TYPES,
                                   verbose_name=_('Tipo de socia'))
    account = models.ForeignKey(Account, null=True, verbose_name=_('Datos de socia'))
    name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Nombre'))
    contact_person = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Persona de contacto'))
    contact_phone = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Teléfono de contacto'))
    contact_email = models.EmailField(null=False, verbose_name=_('Email de contacto'))

    last_update = models.DateTimeField(auto_now=True, verbose_name=_('Última actualización'))

    objects = SignupsManager()


    class Meta:
        verbose_name = _('Proceso de acogida')
        verbose_name_plural = _('Procesos de acogida')
        permissions = (
            ("mespermission_can_view_signups", _("Puede ver los procesos de acogida pendientes")),
            ("mespermission_can_create_signups", _("Puede añadir nuevos procesos de acogida")),
            ("mespermission_can_comment_signups", _("Puede añadir comentarios a un proceso de acogida")),
            ("mespermission_can_update_signups", _("Puede actualizar el estado de un proceso de acogida")),
        )

    def __str__(self):
        if self.account:
            return self.account.display_name.encode('utf-8')
        else:
            return "{}".format(self.uuid).encode('utf-8')


    def is_in_payment_step(self):
        if self.workflow.current_state is None:
            return False

        return self.workflow.current_state.is_named_step(STEP_PAYMENT) or self.workflow.current_state.is_named_step(STEP_CONSUMER_PAYMENT)

    def initialize(self):

        if self.member_type == settings.MEMBER_PROV:
            process = CurrentProcess.objects.filter(shortname='prov_signup').first().process

        if self.member_type == settings.MEMBER_CONSUMER:
            process = CurrentProcess.objects.filter(shortname='cons_signup').first().process

        workflow = ProcessWorkflow()
        workflow.process = process
        workflow.current_state = workflow.get_first_step()
        workflow.save()
        self.workflow = workflow
        self.save()

    def should_show_payment(self):
        if self.account.get_real_instance_class() is Consumer:
            if self.is_in_payment_step():
                return self.account.pay_by_debit == False

    def form_filled(self, account):

        account.status = SIGNUP
        account.save()

        self.account = account
        self.save()

        if account.get_real_instance_class() is Provider:
            process = CurrentProcess.objects.filter(shortname='prov_signup').first().process
            step = CurrentProcessStep.objects.filter(process=process, shortname=STEP_SIGNUP_FORM).first().process_step

            if self.workflow.is_first_step():
                self.workflow.complete_current_step()
                self.workflow.current_state = step
                self.workflow.add_comment(user=None, comment='La entidad completa el formulario')


        if account.get_real_instance_class() is Consumer:
            process = CurrentProcess.objects.filter(shortname='cons_signup').first().process
            step = CurrentProcessStep.objects.filter(process=process, shortname=STEP_CONSUMER_FORM).first().process_step

            if self.workflow.is_first_step():
                self.workflow.complete_current_step()
                self.workflow.current_state = step
                self.workflow.add_comment(user=None, comment='La consumidora completa el formulario')



@receiver(post_save, sender=ProcessWorkflowEvent)
def update_process_event(sender, instance, **kwargs):
    process = SignupProcess.objects.filter(workflow=instance.workflow).first()
    if process and process.account:
        process.last_update = datetime.now()
        process.save()

        if process.is_in_payment_step():
            # If we just advanced steps and is in the payment step, we create the payment order
            from payments.models import PendingPayment
            PendingPayment.objects.create_initial_payment(process.account)

        if instance.step:
            if instance.step.is_named_step(STEP_SIGNUP_FORM) or instance.step.is_named_step(STEP_CONSUMER_FORM):
                process.account.status = INITIAL_PAYMENT
                process.account.registration_date = datetime.now()
                process.account.save()

            if instance.step.is_named_step(STEP_PAYMENT) or instance.step.is_named_step(STEP_CONSUMER_PAYMENT):
                process.account.status = ACTIVE
                process.account.save()


        if instance.workflow.completed:
            from currency.models import CurrencyAppUser
            CurrencyAppUser.objects.create_app_user(process.account)
