from django.core.management.base import BaseCommand

from accounts.models import Provider
from payments.models import PendingPayment


class Command(BaseCommand):
    help = 'Create Entity AccountAnnualFeeCharge and paymments for fee and social capital'

    def add_arguments(self, parser):
        parser.add_argument('entity_id', type=int, help='Entity ID')


    def handle(self, *args, **options):

        entity_id = options['entity_id']
        provider = Provider.objects.get(pk=entity_id)
        if provider:
            print(f'Provider found: {provider}')
            PendingPayment.objects.create_initial_payment(provider)
        else:
            print('Provider not found')
