# -*- coding: utf-8 -*-

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

        # Entities (Providers and Colaborators) with collaboration agreement
        entities = Entity.objects.active().filter(entity_colabs__isnull=False,
                                                  entity_colabs__custom_fee__isnull=False, entity_colabs__custom_fee__gt=0)

        """ 
        TODO Previous filter should add registration_date__year__lt=year, to avoid autogenerate payments for entities 
        registered the current year. But there is a bug in Colaborators and registration_date is not being auto generating
        """

        print(f'Entities with non 0€ collaboration: {len(entities)}')

        for entity in entities:
            entity_colabs = entity.entity_colabs.all()
            print(f'\nEntity {entity.display_name}. Collaborations: {len(entity_colabs)}')
            for entity_colab in entity_colabs:
                fee = entity_colab.custom_fee
                if fee:
                    charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=entity, annual_charge=annual_charge, collab=entity_colab)
                    if not charge.split and not charge.payment:
                        concept = entity_colab.fee_concept(year)
                        charge.payment = PendingPayment.objects.create(concept=concept, account=entity, amount=fee)
                        charge.amount = fee
                        charge.save()
                    else:
                        print(f'Entity fee already exists: {entity.display_name}')
                else:
                    print(f'Non fee: {fee}')



