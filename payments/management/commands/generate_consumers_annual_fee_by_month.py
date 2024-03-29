# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from accounts.models import Consumer
from core.models import User
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges, PendingPayment, SepaPaymentsBatch, SepaBatchResult
import datetime


class Command(BaseCommand):
    help = 'Generate annual fee charges for Consumers by month'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=User, help='User that started the request', default=None)
        parser.add_argument('--year', type=int, help='Year of annual fee charges', default=datetime.datetime.now().year)

    def handle(self, *args, **options):

        current_year = options.get("year")
        current_month = datetime.datetime.now().month

        consumers = (Consumer.objects.active()
                     .filter(registration_date__gte=datetime.date(2023, 10, 1))
                     .filter(registration_date__year__lt=current_year)
                     .filter(registration_date__month__lte=current_month))

        annual_charge, created = AnnualFeeCharges.objects.get_or_create(year=current_year)

        total = len(consumers)

        print("Consumidoras: {}".format(len(consumers)))

        sepa = SepaPaymentsBatch.objects.create(title="Cuotas anuales consumidoras {}/{}".format(current_month, current_year))

        order = 1

        for index, consumer in enumerate(consumers):
            charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=consumer, annual_charge=annual_charge, collab=None)

            if not created:
                print("Consumer {} already has annual fee charge created".format(consumer.display_name))
                continue

            fee = consumer.current_fee
            if fee is not None:
                if not charge.split and not charge.payment:
                    print(f'Consumer {index+1} of {total}', end="\r")
                    concept = consumer.fee_concept(current_year)
                    charge.payment = PendingPayment.objects.create(concept=concept, account=consumer, amount=fee)
                    charge.amount = fee
                    charge.save()
                    sepa.payments.add(charge.payment)
                    SepaBatchResult.objects.update_or_create(
                        payment=charge.payment,
                        batch=sepa,
                        defaults={'order': order}
                    )
                    order += 1
                else:
                    print(f'Consumer fee already created: {consumer.display_name}')
            else:
                print(f'Fee is None for {consumer.display_name}')

        if sepa.payments.exists():
            sepa.amount = sum(payment.amount for payment in sepa.payments.all())
            sepa.generated_by = options.get("user")
            sepa.preprocess_batch()
            sepa.generate_batch()
            sepa.save()
        else:
            sepa.delete()

        print("")

