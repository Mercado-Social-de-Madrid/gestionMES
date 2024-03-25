# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from accounts.models import Provider
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges, PendingPayment, SepaPaymentsBatch, \
    SepaBatchResult, PROVIDERS, AutogeneratedAnnualFee


class Command(BaseCommand):
    help = 'Generate annual fee charges for Providers'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='Year for annual fee charges generation')
        parser.add_argument('generate-sepa', type=bool, default=False, nargs='?', help='Autocreate sepa batch with all fee charges')


    def handle(self, *args, **options):

        year = options['year']
        generate_sepa = options.get('generate-sepa')

        providers = Provider.objects.active().filter(registration_date__year__lt=year)
        annual_charge, created = AnnualFeeCharges.objects.get_or_create(year=year)

        total = len(providers)

        if generate_sepa:
            sepa = SepaPaymentsBatch.objects.create(title="Cuotas anuales proveedoras " + str(year))

        order = 1

        for index, provider in enumerate(providers):
            charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=provider, annual_charge=annual_charge, collab=None)
            fee = provider.current_fee
            if fee is not None and fee > 0:
                if not provider.payment_in_kind:
                    if not charge.split and not charge.payment:
                        print(f'Provider {index+1} of {total}', end="\r")
                        concept = provider.fee_concept(year)
                        charge.payment = PendingPayment.objects.create(concept=concept, account=provider, amount=fee)
                        charge.amount = fee
                        charge.save()

                        if generate_sepa:
                            sepa.payments.add(charge.payment)
                            SepaBatchResult.objects.update_or_create(
                                payment=charge.payment,
                                batch=sepa,
                                defaults={'order': order}
                            )
                            order += 1
                    else:
                        print(f'Provider fee already created: {provider.display_name}')
                else:
                    print(f'Provider payment in kink: {provider.display_name}')
            else:
                print(f'Fee is None or 0 for {provider.display_name}')


        if generate_sepa:
            if sepa.payments.exists():
                print("Preparing SEPA...")
                sepa.amount = sum(payment.amount for payment in sepa.payments.all())
                sepa.generated_by = options.get("user")
                sepa.preprocess_batch()
                sepa.generate_batch()
                sepa.save()
            else:
                sepa.delete()

        AutogeneratedAnnualFee.objects.create(year=year, account_type=PROVIDERS)

        print("")

