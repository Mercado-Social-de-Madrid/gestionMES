# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from accounts.models import Consumer
from core.models import User
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges, PendingPayment, SepaPaymentsBatch, \
    SepaBatchResult, AutogeneratedAnnualFee, CONSUMERS
import datetime


class Command(BaseCommand):
    help = 'Generate annual fee charges for Consumers'

    def add_arguments(self, parser):
        parser.add_argument('sepa_id', type=int, help='Sepa ID')

    def handle(self, *args, **options):

        sepa_id = options.get("sepa_id")

        sepa = SepaPaymentsBatch.objects.get(pk=sepa_id)

        count = len(sepa.payments.all())
        print(f"Payments: {count}")


        for index, payment in enumerate(sepa.payments.all()):
            print(f'Deleting payment and charge: {index + 1} of {count}', end="\r")
            try:
                charge = AccountAnnualFeeCharge.objects.get(payment=payment)
                charge.delete()
            except ObjectDoesNotExist:
                print(f"\nCuota no encontrada: {payment.account.cif}")

            payment.delete()

