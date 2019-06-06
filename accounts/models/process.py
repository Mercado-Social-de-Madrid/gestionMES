# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from accounts.models import Provider, Consumer, Account, INITIAL_PAYMENT, ACTIVE, OPTED_OUT, SIGNUP
from payments.models import PendingPayment
from simple_bpm.models import ProcessWorkflow, CurrentProcess, CurrentProcessStep, ProcessWorkflowEvent

STEP_SIGNUP_FORM = 'signup_form'
STEP_CONSUMER_FORM = 'consumer_form'
STEP_PAYMENT_RULES = 'payment_rules'
STEP_PAYMENT = 'payment'
STEP_CONSUMER_PAYMENT = 'consumer_payment'


class AccountProcess(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, auto_created=True, verbose_name=_('Identificador proceso'))
    workflow = models.ForeignKey(ProcessWorkflow, null=True, verbose_name=_('Seguimiento del proceso'))
    last_update = models.DateTimeField(auto_now=True, verbose_name=_('Última actualización'))
    member_type = models.CharField(null=True, blank=True, max_length=30, choices=settings.MEMBER_TYPES,
                                   verbose_name=_('Tipo de socia'))
    cancelled = models.BooleanField(default=False, verbose_name=_('Cancelado'))

    provider_process = None
    consumer_process = None
    general_process = None

    class Meta:
        abstract = True

    def initialize(self):

        if self.provider_process and self.member_type == settings.MEMBER_PROV:
            process = CurrentProcess.objects.filter(shortname=self.provider_process).first().process
        elif self.consumer_process and self.member_type == settings.MEMBER_CONSUMER:
            process = CurrentProcess.objects.filter(shortname=self.consumer_process).first().process
        else:
            process = CurrentProcess.objects.filter(shortname=self.general_process).first().process

        workflow = ProcessWorkflow()
        workflow.process = process
        workflow.current_state = workflow.get_first_step()
        workflow.save()
        self.workflow = workflow
        self.save()


    def __str__(self):
        if hasattr(self, 'account') and self.account:
            return self.account.display_name.encode('utf-8')
        else:
            return "{}".format(self.uuid).encode('utf-8')



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


class SignupProcess(AccountProcess):

    account = models.ForeignKey(Account, null=True, verbose_name=_('Datos de socia'), related_name='signup_process')
    name = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Nombre'))
    contact_person = models.CharField(null=True, blank=True, max_length=250, verbose_name=_('Persona de contacto'))
    contact_phone = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Teléfono de contacto'))
    contact_email = models.EmailField(null=False, verbose_name=_('Email de contacto'))

    objects = SignupsManager()

    provider_process = 'prov_signup'
    consumer_process = 'cons_signup'

    class Meta:
        verbose_name = _('Proceso de acogida')
        verbose_name_plural = _('Procesos de acogida')
        permissions = (
            ("mespermission_can_view_signups", _("Puede ver los procesos de acogida pendientes")),
            ("mespermission_can_create_signups", _("Puede añadir nuevos procesos de acogida")),
            ("mespermission_can_comment_signups", _("Puede añadir comentarios a un proceso de acogida")),
            ("mespermission_can_update_signups", _("Puede actualizar el estado de un proceso de acogida")),
        )


    def is_in_payment_step(self):
        if self.workflow.current_state is None:
            return False

        return self.workflow.current_state.is_named_step(STEP_PAYMENT) or self.workflow.current_state.is_named_step(STEP_CONSUMER_PAYMENT)


    def should_show_payment(self):
        if self.account.get_real_instance_class() is Consumer:
            if self.is_in_payment_step():
                return self.account.pay_by_debit == False


    def update(self, event):
        if self.is_in_payment_step():
            # If we just advanced steps and is in the payment step, we create the payment order
            from payments.models import PendingPayment
            PendingPayment.objects.create_initial_payment(self.account)

        if event.step:
            if event.step.is_named_step(STEP_SIGNUP_FORM) or event.step.is_named_step(STEP_CONSUMER_FORM):
                self.account.status = INITIAL_PAYMENT
                self.account.registration_date = datetime.now()
                self.account.save()

            if event.step.is_named_step(STEP_PAYMENT) or event.step.is_named_step(STEP_CONSUMER_PAYMENT):
                self.account.status = ACTIVE
                self.account.save()


        if event.workflow.completed:
            from currency.models import CurrencyAppUser
            CurrencyAppUser.objects.create_app_user(self.account)


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


    def cancel(self):
        self.last_update = datetime.now()
        self.cancelled = True
        self.save()

        if self.account:
            self.account.status = OPTED_OUT
            self.account.save()

            # Remove any pending payments as well
            PendingPayment.objects.filter(account=self.account).delete()


class DeletionManager(models.Manager):

    def pending(query, entity=None):
        return query.filter(workflow__completed=False)

    def create_process(self, account):
        deletion, created = self.get_or_create(account=account, member_type=account.member_type)
        if created:
            deletion.initialize()
        return deletion


class DeletionProcess(AccountProcess):
    account = models.ForeignKey(Account, null=True, verbose_name=_('Datos de socia'), related_name='deletion_process')

    general_process = 'account_deletion'

    class Meta:
        verbose_name = _('Proceso de baja')
        verbose_name_plural = _('Procesos de baja')
        permissions = (
            ("mespermission_can_view_deletions", _("Puede ver los procesos de baja pendientes")),
            ("mespermission_can_create_deletions", _("Puede añadir nuevos procesos de baja")),
            ("mespermission_can_comment_deletions", _("Puede añadir comentarios a un proceso de baja")),
            ("mespermission_can_update_deletions", _("Puede actualizar el estado de un proceso de baja")),
        )

    objects = DeletionManager()

    def update(self, event):

        if event.workflow.completed:
            self.account.status = OPTED_OUT
            self.account.save()

@receiver(post_save, sender=ProcessWorkflowEvent)
def update_process_event(sender, instance, **kwargs):
    process = SignupProcess.objects.filter(workflow=instance.workflow).first()
    if not process:
        process = DeletionProcess.objects.filter(workflow=instance.workflow).first()

    if process and process.account:
        process.last_update = datetime.now()
        process.save()
        process.update(instance)

