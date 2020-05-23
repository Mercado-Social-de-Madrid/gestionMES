# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _

from accounts.models import Account, UserComment


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

    class Meta:
        verbose_name = _('Rango de cuotas')
        verbose_name_plural = _('Rangos de cuotas')
        ordering = ['min_num_workers', 'max_num_workers', 'min_income', 'max_income']

    def __str__(self):
        return "{} - {}".format(self.min_num_workers, self.max_num_workers).encode('utf-8')

    @staticmethod
    def calculate_fee(account):
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


class FeeComments(UserComment):
    account = models.ForeignKey(Account, related_name='fee_comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['timestamp']
        verbose_name = _('Comentario de cuota')
        verbose_name_plural = _('Comentarios de cuota')

