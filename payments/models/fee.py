# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _

from accounts.models import Account, Provider, Consumer, Colaborator, EntityCollaboration
from core.models import UserComment
from payments.models import PendingPayment


class FeeRange(models.Model):

    min_num_workers = models.IntegerField(default=1, verbose_name=_('Mínimo Número de trabajadoras'))
    max_num_workers = models.IntegerField(default=1, verbose_name=_('Máximo Número de trabajadoras'))
    min_income = models.IntegerField(default=1, verbose_name=_('Ingresos mínimos'))
    max_income = models.IntegerField(default=1, verbose_name=_('Ingresos máximos'))
    fee = models.FloatField(verbose_name=_('Cuota'))

    DEFAULT_PROVIDER_FEE = 100.0
    DEFAULT_CONSUMER_FEE = 20.0
    DEFAULT_PROVIDER_SHARE = 20.0
    DEFAULT_CONSUMER_SHARE = 10.0
    DEFAULT_SPECIAL_FEE = 500.0

    class Meta:
        verbose_name = _('Rango de cuotas')
        verbose_name_plural = _('Rangos de cuotas')
        ordering = ['min_num_workers', 'max_num_workers', 'min_income', 'max_income']

    def __str__(self):
        return "{} - {}".format(self.min_num_workers, self.max_num_workers).encode('utf-8')


    @staticmethod
    def calculate_fee(account):
        if account.get_real_instance_class() is Provider:
            return FeeRange.calculate_provider_fee(account)
        elif account.get_real_instance_class() is Consumer:
            return FeeRange.DEFAULT_CONSUMER_FEE
        elif account.get_real_instance_class() is Colaborator:
            return FeeRange.DEFAULT_SPECIAL_FEE
        else:
            return  None


    @staticmethod
    def calculate_provider_fee(account):
        if account.num_workers == 1 and account.aprox_income == 0:
            return None

        fee_range = FeeRange.objects.filter(
            min_num_workers__lte=account.num_workers,
            max_num_workers__gte=account.num_workers,
            min_income__lte=account.aprox_income,
            max_income__gte=account.aprox_income).first()

        if fee_range:
            return fee_range.fee
        return FeeRange.DEFAULT_PROVIDER_FEE


class AnnualFeeCharges(models.Model):
    year = models.IntegerField(verbose_name=_('Año'))
    accounts = models.ManyToManyField(Account, verbose_name=_('Socias'), through='AccountAnnualFeeCharge', related_name='annual_fee_charges')

    class Meta:
        ordering = ['-year']
        verbose_name = _('Cobro anual de cuota')
        verbose_name_plural = _('Cobros anuales de cuota')

    def create_pending_data(self):
        for account in Account.objects.active().filter(registration_date__year__lt=self.year):
            charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=account, annual_charge=self, collab=None)
            fee = account.current_fee
            if fee is not None and fee > 0:
                if charge.amount == 0:
                    charge.amount = fee
                    charge.save()
                if not charge.payment:
                    concept = "Cuota anual {}".format(self.year)
                    charge.payment = PendingPayment.objects.create(
                        concept=concept, account=account, amount = fee)
                    charge.amount = fee
                    charge.save()
                elif not charge.payment.is_completed and not charge.manually_modified and charge.payment.amount != fee:
                    # if the payment is not done yet and the fee has changed, update it
                    charge.amount = fee
                    charge.payment.amount = fee
                    charge.payment.save()
                    charge.save()

        for collab in EntityCollaboration.objects.all():
            fee = collab.custom_fee or collab.collaboration.default_fee
            if fee is not None and fee > 0:
                charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=collab.entity,
                                                                               annual_charge=self, collab=collab)
                if charge.amount == 0:
                    charge.amount = fee
                    charge.save()
                if not charge.payment:
                    concept = "Cuota anual {}({})".format(self.year, collab.collaboration.name)
                    charge.payment = PendingPayment.objects.create(
                        concept=concept, account=collab.entity, amount=fee)
                    charge.amount = fee
                    charge.save()
                elif not charge.payment.is_completed and not charge.manually_modified and charge.payment.amount != fee:
                    # if the payment is not done yet and the fee has changed, update it
                    charge.amount = fee
                    charge.save()
                    charge.payment.amount = fee
                    charge.payment.save()


class AccountAnnualFeeCharge(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    collab = models.ForeignKey(EntityCollaboration, null=True, on_delete=models.SET_NULL, related_name='fee_charges')
    annual_charge = models.ForeignKey(AnnualFeeCharges, on_delete=models.CASCADE, )
    amount = models.FloatField(default=0, verbose_name=_('Cantidad'))
    payment = models.ForeignKey(PendingPayment, null=True, on_delete=models.SET_NULL, related_name='fee_charges')
    payments = models.ManyToManyField(PendingPayment, related_name='fee_split_charges')
    split = models.BooleanField(default=False, verbose_name=_('Pago fraccionado'))
    manually_modified = models.BooleanField(default=False, verbose_name=_('Modificado manualmente'))
    comments = models.TextField(blank=True, null=True, verbose_name=_('Comentarios'))

    class Meta:
        verbose_name = _('Cobro anual de cuota a socia')
        verbose_name_plural = _('Cobros anuales de cuota a socias')

    def payment_updated(self):
        calculated_amount = self.account.current_fee
        if self.payment:
            self.amount = self.payment.amount

        self.manually_modified =  calculated_amount != self.amount

        self.save()


class FeeComments(UserComment):
    account = models.ForeignKey(Account, related_name='fee_comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['timestamp']
        verbose_name = _('Comentario de cuota')
        verbose_name_plural = _('Comentarios de cuota')

