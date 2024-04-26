# -*- coding: utf-8 -*-

from datetime import datetime

from django.core.management.base import BaseCommand

from accounts.models import Provider
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges


class Command(BaseCommand):
    help = 'Check Providers corresponding fee with generated annual fee (in case that workers or incomes were modified after fee generation)'

    def handle(self, *args, **options):

        providers = Provider.objects.active()

        year = datetime.now().year
        annual_charge = AnnualFeeCharges.objects.get(year=year)

        for provider in providers:

            try:
                charge = AccountAnnualFeeCharge.objects.get(account=provider, annual_charge=annual_charge, collab=None)
                if charge.amount != provider.corresponding_fee and charge.amount != provider.custom_fee:
                    print(f'{provider.name} - Annual fee charge does not match. Actual annual fee: '
                          f'{charge.amount}, corresponding fee: {provider.corresponding_fee}')
            except AccountAnnualFeeCharge.DoesNotExist:
                # print(f'{provider.name} - does not have annual fee charge for {year}')
                pass
