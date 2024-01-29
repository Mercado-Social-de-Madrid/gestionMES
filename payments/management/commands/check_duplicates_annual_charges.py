# -*- coding: utf-8 -*-
import datetime

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.management.base import BaseCommand

from accounts.models import Consumer
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges


class Command(BaseCommand):
    help = 'Generate annual fee charges for Consumers'

    def add_arguments(self, parser):
        parser.add_argument('--year', type=int, help='Year of annual fee charges', default=datetime.datetime.now().year)
        parser.add_argument('--clean', type=bool, help='True for deleting duplicates', default=False)

    def handle(self, *args, **options):

        current_year = options.get("year")
        clean = options.get("clean")

        consumers = Consumer.objects.active()

        annual_charge = AnnualFeeCharges.objects.get(year=current_year)

        for index, consumer in enumerate(consumers):
            charges = AccountAnnualFeeCharge.objects.filter(account=consumer, annual_charge=annual_charge, collab=None)
            if len(charges) > 1:
                print(f"Charge duplicated. Consumer: {consumer.display_name} - {consumer.cif}")
                if clean:
                    first_skipped = False
                    for charge in charges:
                        if not first_skipped:
                            first_skipped = True
                            continue
                        else:
                            charge.payment.delete()
                            charge.delete()



