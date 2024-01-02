# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from accounts.models import Consumer, Provider
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges, PendingPayment, SepaPaymentsBatch


class Command(BaseCommand):
    help = 'Generate annual fee charges for Providers'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='Year for annual fee charges generation')

    def handle(self, *args, **options):

        year = options['year']
        providers = Provider.objects.active().filter(registration_date__year__lt=year)
        annual_charge, created = AnnualFeeCharges.objects.get_or_create(year=year)

        total = len(providers)

        sepa = SepaPaymentsBatch.objects.create(title="Cuotas anuales proveedoras " + str(year))

        for index, provider in enumerate(providers):
            charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=provider, annual_charge=annual_charge, collab=None)
            fee = provider.current_fee
            if fee is not None:
                if not charge.split and not charge.payment:
                    print(f'Provider {index+1} of {total}', end="\r")
                    concept = provider.fee_concept(year)
                    charge.payment = PendingPayment.objects.create(concept=concept, account=provider, amount=fee)
                    charge.amount = fee
                    charge.save()
                    sepa.payments.add(charge.payment)
                else:
                    print(f'Consumer fee already created: {provider.display_name}')
            else:
                print(f'Fee is None for {provider.display_name}')

        if sepa.payments.exists():
            sepa.amount = sum(payment.amount for payment in sepa.payments.all())
            sepa.generated_by = options.get("user")
            sepa.save()
        else:
            sepa.delete()

        print("")

