# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
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

from accounts.models import Account, Provider, Consumer
from core.models import User
from currency_server import wallet_transaction
from helpers import RandomFileName
from mes import settings
from sermepa.models import SermepaResponse
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

DEFAULT_PROVIDER_FEE = 100.0
DEFAULT_CONSUMER_FEE = 20.0

DEFAULT_PROVIDER_SHARE = 20.0
DEFAULT_CONSUMER_SHARE = 10.0

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

    @staticmethod
    def calculate_fee(account):

        fee_range = FeeRange.objects.filter(
            min_num_workers__lte=account.num_workers,
            max_num_workers__gte=account.num_workers,
            min_income__lte=account.aprox_income,
            max_income__gte=account.aprox_income).first()

        if fee_range:
            return fee_range.fee
        return DEFAULT_PROVIDER_FEE



class PaymentsManager(models.Manager):

    def create_initial_payment(self, account):
        payment, created =  PendingPayment.objects.get_or_create(account=account)
        if account.get_real_instance_class() is Provider:
            fee = FeeRange.calculate_fee(account)
            share = DEFAULT_PROVIDER_SHARE
        else:
            fee = DEFAULT_CONSUMER_FEE
            share = DEFAULT_CONSUMER_SHARE

        print('Creating initial payment!')
        amount = fee + share
        payment.concept = "Pago inicial: {}€ ({} capital social + {} cuota anual)".format(amount, share, fee)
        payment.amount = amount
        if account.pay_by_debit == True:
            payment.type = DEBIT

        payment.save()

        return payment

    def get_card_payment(self, reference):
        try:
            card_payment = CardPayment.objects.filter(reference=reference)
            if card_payment.exists():
                return card_payment.first(), False

            # If the reference is related to a payment, we create a new card payment
            payment = self.filter(reference=reference)
            if payment.exists():
                payment = payment.first()
                if not payment.completed:
                    card_payment = CardPayment.objects.create(
                        account=payment.account,
                        type=PENDING_PAYMENT,
                        pending_payment=payment,
                        amount=payment.amount
                    )
                    return card_payment, False
                else:
                    return payment, True
        except ValidationError:
            # In case a wrong UUID format is passed
            pass

        return None, False


    def process_sermepa_payment(self, sermepa_response):
        card_payment = CardPayment.objects.get(pk=sermepa_response.Ds_MerchantData)
        card_payment.bank_response = sermepa_response
        card_payment.paid = True
        card_payment.save()

        if card_payment.type == CURRENCY_BUY:
            # We are buying new currency, should process it accordingly
            success, uuid = wallet_transaction.add_transaction(
                account=card_payment.account,
                amount=float(card_payment.amount),
                concept='Compra de etics')

            if success:
                print(uuid)

        elif card_payment.type == PENDING_PAYMENT and card_payment.pending_payment:
            # The card payment was related to a pending payment, so we set it as paid
            card_payment.pending_payment.paid_by_card()


    def currency_purchase(self, account, amount):

        card_payment = CardPayment.objects.create(
            account=account,
            amount=amount,
            type = CURRENCY_BUY
        )

        return card_payment


class PendingPayment(models.Model):

    account = models.ForeignKey(Account, null=True, related_name='pending_payments', verbose_name=_('Socia'), on_delete=models.CASCADE)
    revised_by = models.ForeignKey(User, null=True, verbose_name=_('Usuario que revisó'), on_delete=models.SET_NULL)
    type = models.CharField(null=True, blank=True, max_length=30, choices=PAYMENT_METHODS,
                                   verbose_name=_('Modo de pago'))
    amount = models.FloatField(default=0, verbose_name=_('Cantidad'))
    concept = models.TextField(null=True, blank=True, verbose_name=_('Concepto'))
    added = models.DateTimeField(auto_now_add=True, verbose_name=_('Añadido'))
    completed = models.BooleanField(default=False, verbose_name=_('Realizado'))
    timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha pago'))
    comment = models.TextField(null=True, blank=True, verbose_name=_('Comentario'))
    reference = models.UUIDField(default=uuid.uuid4, auto_created=True, verbose_name=_('Referencia del pago'))

    objects = PaymentsManager()

    class Meta:
        verbose_name = _('Pago pendiente')
        verbose_name_plural = _('Pagos pendientes')
        ordering = ['added']

    @property
    def icon_name(self):
        if not self.type:
            return ''
        elif self.type == CREDIT_CARD:
            return 'credit_card'
        elif self.type == DEBIT:
            return 'receipt'
        elif self.type == TRANSFER:
            return 'local_atm'

    def paid_by_card(self):
        self.completed = True
        self.type = CREDIT_CARD
        self.timestamp = datetime.now()
        self.save()

        #TODO: Notify/update signup process...

    def __str__(self):
        return '{}:{}'.format(self.account.display_name, self.amount).encode('utf-8')


class CardPayment(models.Model):
    account = models.ForeignKey(Account, null=True, related_name='card_payments', verbose_name=_('Socia'), on_delete=models.CASCADE)
    attempt = models.DateTimeField(auto_now_add=True, verbose_name=_('Añadido'))
    amount = models.FloatField(default=0, verbose_name=_('Cantidad'))
    reference = models.UUIDField(default=uuid.uuid4, auto_created=True, verbose_name=_('Referencia del pago'))
    bank_response = models.ForeignKey(SermepaResponse, null=True, blank=True, verbose_name=_('Respuesta TPV'), on_delete=models.SET_NULL)
    pending_payment = models.ForeignKey(PendingPayment, null=True, blank=True, verbose_name=_('Pago pendiente'), on_delete=models.SET_NULL)
    type = models.CharField(null=True, blank=True, max_length=30, choices=CARD_PAYMENT_TYPES, verbose_name=_('Tipo de pago'))
    paid = models.BooleanField(default=False, verbose_name=_('Pago completado'))

    class Meta:
        verbose_name = _('Pago con tarjeta')
        verbose_name_plural = _('Pagos con tarjeta')
        ordering = ['attempt']

    @property
    def concept(self):
        if self.type == PENDING_PAYMENT:
            return self.pending_payment.concept
        elif self.type == CURRENCY_BUY:
            return  'Compra ({} etics)'.format(self.amount)
        else:
            return ''