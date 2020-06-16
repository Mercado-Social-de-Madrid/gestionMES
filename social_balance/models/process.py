# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from accounts.models import Provider, Consumer, Account, INITIAL_PAYMENT, ACTIVE, OPTED_OUT, SIGNUP, AccountProcess, \
    Entity
from core.models import User
from payments.models import PendingPayment
from simple_bpm.models import ProcessWorkflow, CurrentProcess, CurrentProcessStep, ProcessWorkflowEvent

STEP_SIGNUP_FORM = 'signup_form'
STEP_CONSUMER_FORM = 'consumer_form'
STEP_PAYMENT_RULES = 'payment_rules'
STEP_PAYMENT = 'payment'
STEP_CONSUMER_PAYMENT = 'consumer_payment'



class BalanceManager(models.Manager):

    def pending(query, year=None):
        if year:
            return query.filter(workflow__completed=False, year=year)
        else:
            return query.filter(workflow__completed=False)

    def create_pending_processes(self, year):
        for account in Entity.objects.active():
            process, created = self.get_or_create(account=account, year=year)
            if created:
                process.initialize()

    def create_process(self, account):
        process, created = self.get_or_create(account=account, member_type=account.member_type)
        if created:
            process.initialize()

        return process


class BalanceProcess(AccountProcess):
    account = models.ForeignKey(Account, null=True, verbose_name=_('Datos de socia'), related_name='balance_process', on_delete=models.CASCADE)
    sponsor = models.ForeignKey(User, null=True, verbose_name=_('Madrina'), related_name='balance_sponsors', on_delete=models.SET_NULL)
    year = models.SmallIntegerField(default=2019, blank=False, null=False, verbose_name=_('Año'))

    general_process = 'social_balance'

    class Meta:
        verbose_name = _('Proceso de balance social')
        verbose_name_plural = _('Procesos de balance social')
        permissions = (
            ("mespermission_can_manage_balance_process", _("Puede gestionar los procesos de balance social")),
            ("mespermission_can_add_balance_comments", _("Puede añadir comentarios a un proceso de balance social")),
            ("mespermission_can_view_balance_process", _("Puede ver los procesos de balance social")),
        )

    objects = BalanceManager()

    def update(self, event):
        if event.workflow.completed:
            pass



@receiver(post_save, sender=ProcessWorkflowEvent)
def update_process_event(sender, instance, **kwargs):
    #special event types should be ignored by concrete processes
    if instance.special:
        return

    process = BalanceManager.objects.filter(workflow=instance.workflow).first()
    if not process:
        return

    if process and process.account:
        process.last_update = datetime.now()
        process.save()
        process.update(instance)

