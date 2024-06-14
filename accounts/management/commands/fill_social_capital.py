
from django.core.management.base import BaseCommand

from accounts.models import Provider, Consumer, SocialCapital
from settings import constants
from settings.models import SettingProperties


class Command(BaseCommand):
    help = 'Fill Provider custom_fee field with FeeRange calculator'

    def handle(self, *args, **options):
        providers = Provider.objects.all()
        consumers = Consumer.objects.all()

        total = len(providers) + len(consumers)
        actual = 0

        for prov in providers:
            actual += 1
            print(f'Processing {actual} of {total}')
            social_capital = SettingProperties.float_value(constants.PAYMENTS_DEFAULT_PROVIDER_SOCIAL_CAPITAL)
            prov.social_capital = SocialCapital.objects.create(amount=social_capital)
            prov.save()

        for consumer in consumers:
            actual += 1
            print(f'Processing {actual} of {total}')
            social_capital = SettingProperties.float_value(constants.PAYMENTS_DEFAULT_CONSUMER_SOCIAL_CAPITAL)
            consumer.social_capital = SocialCapital.objects.create(amount=social_capital)
            consumer.save()
