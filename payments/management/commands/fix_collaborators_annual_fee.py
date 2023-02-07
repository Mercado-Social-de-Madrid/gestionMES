# -*- coding: utf-8 -*-
import datetime

from django.core.management.base import BaseCommand

from accounts.models import Entity, Colaborator
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges, PendingPayment


class Command(BaseCommand):
    help = 'Generate annual fee charges for Collaboration agreements (special entities, Providers and Collaborators)'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='Year for annual fee charges generation')

    def handle(self, *args, **options):

        year = options['year']
        annual_charge, created = AnnualFeeCharges.objects.get_or_create(year=year)

        # Collaborators
        collaborators = Colaborator.objects.filter(custom_fee__isnull=False, custom_fee__gt=0)
        print(f'\nCollaborators with non 0€ fee: {len(collaborators)}\n')
        for collaborator in collaborators:

            print(f'\n{collaborator.display_name}. ')

            charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=collaborator, annual_charge=annual_charge,
                                                                           collab=None)
            if created:
                print('This should not be created!')

            charge.payment.delete()
            print(f'payment deleted')
            charge.delete()
            print("Charge deleted")



            entity_colabs = collaborator.entity_colabs.all()
            print(f'\nGenerating fee {collaborator.display_name}. Collaborations: {len(entity_colabs)}')
            for entity_colab in entity_colabs:
                fee = entity_colab.custom_fee
                if fee:
                    charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=collaborator, annual_charge=annual_charge, collab=entity_colab)
                    if not charge.split and not charge.payment:
                        concept = entity_colab.fee_concept(year)
                        charge.payment = PendingPayment.objects.create(concept=concept, account=collaborator, amount=fee)
                        charge.amount = fee
                        charge.save()
                    else:
                        print(f'Entity fee already exists: {collaborator.display_name}')
                else:
                    print(f'Non fee: {fee}')





