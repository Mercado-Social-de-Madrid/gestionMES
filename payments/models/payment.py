# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

import uuid
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from accounts.models import Account
from core.models import User
from currency_server import wallet_transaction
from sermepa.models import SermepaResponse
from payments.models.payment_constants import *
import logging

from settings import constants
from settings.models import SettingProperties

log = logging.getLogger(__name__)

class PaymentsManager(models.Manager):

    @staticmethod
    def create_initial_payment(account):

        # This is a workaround to solve a bug in which an initial payment is created twice for consumers
        social_capital_already_created = PendingPayment.objects.filter(account=account, is_social_capital=True).first()
        if social_capital_already_created:
            return

        # Two different payments: Social capital and fee

        social_capital_payment = PendingPayment.objects.create(account=account)

        # This checking is temporal. It can be removed if Social capital null error is not happening again
        if not account.social_capital.amount:
            log.warning(f'Social capital is null. Account {account}')
            from accounts.models import Consumer
            if isinstance(account, Consumer):
                account.social_capital.amount = SettingProperties.get_float(constants.PAYMENTS_DEFAULT_CONSUMER_SOCIAL_CAPITAL)
            else:
                account.social_capital.amount = SettingProperties.get_float(constants.PAYMENTS_DEFAULT_PROVIDER_SOCIAL_CAPITAL)

            account.social_capital.save()
        # ---------------------------------

        social_capital_payment.amount = account.social_capital.amount

        social_capital_payment.concept = _("Capital social")
        social_capital_payment.is_social_capital = True

        if account.pay_by_debit:
            social_capital_payment.type = DEBIT

        social_capital_payment.save()

        fee_payment = PendingPayment.objects.create(account=account)
        fee_payment.amount = account.current_fee
        fee_payment.concept = account.fee_concept(settings.CURRENT_FEECHARGES_YEAR)

        if account.pay_by_debit:
            fee_payment.type = DEBIT

        fee_payment.save()

        # Add payment to annual fee charge
        from payments.models import AnnualFeeCharges, AccountAnnualFeeCharge
        annual_charge, created = AnnualFeeCharges.objects.get_or_create(year=settings.CURRENT_FEECHARGES_YEAR)
        charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=account, annual_charge=annual_charge, collab=None)
        charge.payment = fee_payment
        charge.amount = fee_payment.amount
        charge.save()

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
    revised_by = models.ForeignKey(User, null=True, blank=True, verbose_name=_('Usuario que revisó'), on_delete=models.SET_NULL)
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

    invoice_prefix = models.CharField(null=True, blank=True, verbose_name=_('Serie facturación'), max_length=20)
    invoice_number = models.IntegerField(default=1, verbose_name=_('Número de facturación'))
    invoice_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Fecha de factura'))

    is_social_capital = models.BooleanField(default=False, verbose_name=_('Es Capital Social'))

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

    @property
    def invoice_code(self):
        prefix = self.invoice_prefix if self.invoice_prefix else '-'
        return '{}{}{:03d}'.format(self.added.year, prefix, self.invoice_number)

    @property
    def detail_url(self):
        return 'payments:payment_detail'

    @property
    def related_fee(self):
        split_fee = self.fee_split_charges.all().first()
        if split_fee is not None:
            return split_fee
        return self.fee_charges.all().first()

    def paid_by_card(self):
        self.completed = True
        self.type = CREDIT_CARD
        self.timestamp = datetime.now()
        self.save()

        #TODO: Notify/update signup process...

    def __str__(self):
        return '{}:{}'.format(self.account.display_name, self.amount)


# If this payment is linked to Capital social, modify also the capital social of the account
@receiver(post_save, sender=PendingPayment)
def update_social_capital(sender, instance, created, **kwargs):
    if instance.is_social_capital:
        instance.account.social_capital.amount = instance.amount
        instance.account.social_capital.paid = instance.completed
        instance.account.social_capital.paid_timestamp = instance.timestamp
        instance.account.social_capital.paid_type = instance.type
        instance.account.social_capital.returned = instance.returned
        instance.account.social_capital.returned_timestamp = instance.returned_timestamp
        instance.account.social_capital.save()


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
        if self.type == PENDING_PAYMENT and self.pending_payment:
            return self.pending_payment.concept
        elif self.type == CURRENCY_BUY:
            return  'Compra ({} etics)'.format(self.amount)
        else:
            return ''