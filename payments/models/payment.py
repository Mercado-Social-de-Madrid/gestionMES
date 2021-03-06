# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from accounts.models import Account, Provider
from core.models import User
from currency_server import wallet_transaction
from sermepa.models import SermepaResponse

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

RETURN_REASONS = (
    ('noexiste', 'Cuenta no existe'),
    ('cancelada','Cuenta cancelada'),
    ('devuelto','Devuelto por cliente'),
    ('sinfondos','Devuelto por el banco (falta de fondos)'),
    ('otros','Otros'),
)


class PaymentsManager(models.Manager):

    def create_initial_payment(self, account):
        payment, created =  PendingPayment.objects.get_or_create(account=account)
        from payments.models import FeeRange
        fee = account.current_fee
        if account.get_real_instance_class() is Provider:
            share = FeeRange.DEFAULT_PROVIDER_SHARE
        else:
            share = FeeRange.DEFAULT_CONSUMER_SHARE

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
    type = models.CharField(null=True, blank=True, max_length=30, choices=PAYMENT_METHODS, verbose_name=_('Modo de pago'))
    amount = models.FloatField(default=0, verbose_name=_('Cantidad'))
    concept = models.TextField(null=True, blank=True, verbose_name=_('Concepto'))
    added = models.DateTimeField(auto_now_add=True, verbose_name=_('Añadido'))
    completed = models.BooleanField(default=False, verbose_name=_('Realizado'))
    timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha pago'))
    comment = models.TextField(null=True, blank=True, verbose_name=_('Comentario'))
    reference = models.UUIDField(default=uuid.uuid4, auto_created=True, verbose_name=_('Referencia del pago'))

    returned = models.BooleanField(default=False, verbose_name=_('Devuelto'))
    returned_timestamp = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha de devolución'))
    returned_reason = models.CharField(null=True, blank=True, max_length=30, choices=RETURN_REASONS, verbose_name=_('Motivo de devolución'))

    objects = PaymentsManager()

    class Meta:
        verbose_name = _('Pago pendiente')
        verbose_name_plural = _('Pagos pendientes')
        ordering = ['added']
        permissions = (
            ("mespermission_can_view_payments", _("Puede ver los pagos de cada socia")),
            ("mespermission_can_edit_payments", _("Puede editar el estado de los pagos")),
        )

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

    @property
    def is_completed(self):
        return self.completed and not self.returned

    @property
    def contact_email(self):
        return self.account.contact_email

    @property
    def contact_phone(self):
        return self.account.contact_phone

    def paid_by_card(self):
        self.completed = True
        self.type = CREDIT_CARD
        self.timestamp = datetime.now()
        self.save()

        #TODO: Notify/update signup process...

    def __str__(self):
        return '{}:{}'.format(self.account.display_name, self.amount)


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
        permissions = (
            ("mespermission_can_view_card_payments", _("Puede ver los pagos con tarjeta")),
        )

    @property
    def concept(self):
        if self.type == PENDING_PAYMENT:
            return self.pending_payment.concept
        elif self.type == CURRENCY_BUY:
            return  'Compra ({} etics)'.format(self.amount)
        else:
            return ''