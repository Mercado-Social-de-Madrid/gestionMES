from django.core.management.base import BaseCommand

from accounts.models import Entity, Consumer, Provider
from currency.models import CurrencyAppUser


class Command(BaseCommand):
    help = 'Check entities and consumers with no app server data. For issue 110.'

    def handle(self, *args, **options):

        entities = Provider.objects.active()
        print("\nChecking entities:")
        for entity in entities:
            app_user = CurrencyAppUser.objects.filter(cif=entity.cif)
            if len(app_user) == 0:
                print(f'Entity {entity.name} does not have app user')
            elif len(app_user) > 1:
                print(f'Entity {entity.name} have {len(app_user)} app users')
            else:
                if not app_user.first().uuid:
                    print(f'Entity {entity.name} have app users but no UUID')


        consumers = Consumer.objects.active()
        print("\nChecking consumers:")
        for consumer in consumers:
            app_user = CurrencyAppUser.objects.filter(cif=consumer.cif)
            if len(app_user) == 0:
                print(f'Consumer {consumer.first_name} {consumer.last_name} does not have app user')
            elif len(app_user) > 1:
                print(f'Consumer {consumer.first_name} {consumer.last_name} have {len(app_user)} app users')
            else:
                if not app_user.first().uuid:
                    print(f'Consumer {consumer.first_name} {consumer.last_name} have app users but no UUID')

