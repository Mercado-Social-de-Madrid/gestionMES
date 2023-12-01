# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from accounts.models import Consumer
from core.models import User
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges, PendingPayment, SepaPaymentsBatch
import datetime


class Command(BaseCommand):
    help = 'Generate annual fee charges for Consumers'

    def add_arguments(self, parser):
        parser.add_argument('--user', type=User, help='User that started the request', default=None)

    def handle(self, *args, **options):

        current_year= datetime.datetime.now().year
        consumers = Consumer.objects.active().filter(registration_date__lt=datetime.date(2023, 10, 1))
        annual_charge, created = AnnualFeeCharges.objects.get_or_create(year=current_year)

        total = len(consumers)

        sepa = SepaPaymentsBatch.objects.create(title="Cuotas anuales " + str(current_year))

        for index, consumer in enumerate(consumers):
            charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=consumer, annual_charge=annual_charge, collab=None)
            fee = consumer.current_fee
            if fee is not None:
                if not charge.split and not charge.payment:
                    print(f'Consumer {index+1} of {total}', end="\r")
                    concept = consumer.fee_concept(current_year)
                    charge.payment = PendingPayment.objects.create(concept=concept, account=consumer, amount=fee)
                    charge.amount = fee
                    charge.save()
                    sepa.payments.add(charge.payment)
                else:
                    print(f'Consumer fee already created: {consumer.display_name}')
            else:
                print(f'Fee is None for {consumer.display_name}')

        if sepa.payments.exists():
            sepa.amount = sum(payment.amount for payment in sepa.payments.all())
            sepa.generated_by = options.get("user")
            sepa.save()
        else:
            sepa.delete()

        print("")

