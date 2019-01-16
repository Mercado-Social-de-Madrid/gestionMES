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

from accounts.models import Account
from core.models import User
from helpers import RandomFileName
from mes import settings
from simple_bpm.models import ProcessWorkflow, CurrentProcess, CurrentProcessStep, ProcessWorkflowEvent

CREDIT_CARD = 'tarjeta'
TRANSFER = 'transferencia'
DEBIT = 'domiciliacion'

PAYMENT_METHODS = (
    (CREDIT_CARD, 'Pago con tarjeta'),
    (TRANSFER, 'Transferencia'),
    (DEBIT, 'Domiciliación bancaria'),
)

PENDING_PAYMENT = 'pago'
CURRENCY_BUY = 'compramoneda'

CARD_PAYMENT_TYPES = (
    (PENDING_PAYMENT, 'Pago pendiente'),
    (CURRENCY_BUY, 'Compra de Etics'),
)


class FeeRange(models.Model):

    min_num_workers = models.IntegerField(default=1, verbose_name=_('Mínimo Número de trabajadoras'))
    max_num_workers = models.IntegerField(default=1, verbose_name=_('Máximo Número de trabajadoras'))
    min_income = models.IntegerField(default=1, verbose_name=_('Ingresos mínimos'))
    max_income = models.IntegerField(default=1, verbose_name=_('Ingresos máximos'))
    fee = models.FloatField(verbose_name=_('Cuota'))

    class Meta:
        verbose_name = _('Rango de cuotas')
        verbose_name_plural = _('Rangos de cuotas')
        ordering = ['min_num_workers', 'max_num_workers', 'min_income', 'max_income']

    def __str__(self):
        return "{} - {}".format(self.min_num_workers, self.max_num_workers).encode('utf-8')


class PendingPayment(models.Model):

    account = models.ForeignKey(Account, null=True, related_name='pending_payments', verbose_name=_('Socia'))
    revised_by = models.ForeignKey(User, null=True, verbose_name=_('Usuario que revisó'))
    type = models.CharField(null=True, blank=True, max_length=30, choices=PAYMENT_METHODS,
                                   verbose_name=_('Modo de pago'))
    amount = models.FloatField(verbose_name=_('Cantidad'))
    concept = models.TextField(null=True, blank=True, verbose_name=_('Concepto'))
    added = models.DateTimeField(auto_now_add=True, verbose_name=_('Añadido'))
    completed = models.BooleanField(default=False, verbose_name=_('Realizado'))
    timestamp = models.DateTimeField(null=True, verbose_name=_('Fecha pago'))


class CardPayment(models.Model):
    type = models.CharField(null=True, blank=True, max_length=30, choices=CARD_PAYMENT_TYPES,
                            verbose_name=_('Tipo'))
    timestamp = models.DateTimeField(null=True, verbose_name=_('Fecha pago'))
