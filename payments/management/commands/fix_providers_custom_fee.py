# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from accounts.models import Consumer, Provider
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges, PendingPayment


class Command(BaseCommand):
    help = 'Check Providers which have same custom and corresponding fee in order to set updated fee correctly'

    def handle(self, *args, **options):

        providers = Provider.objects.active()

        for provider in providers:
            if provider.custom_fee == provider.corresponding_fee:
                provider.custom_fee = None
                provider.save()
                print(f'{provider.name} - Removed custom_fee as it is the same of corresponding_fee')


