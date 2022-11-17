
from django.core.management.base import BaseCommand
from accounts.models import Provider, Consumer, SocialCapital
from payments.models import FeeRange


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
            prov.social_capital = SocialCapital.objects.create(amount=FeeRange.DEFAULT_PROVIDER_SOCIAL_CAPITAL)
            prov.save()

        for consumer in consumers:
            actual += 1
            print(f'Processing {actual} of {total}')
            consumer.social_capital = SocialCapital.objects.create(amount=FeeRange.DEFAULT_CONSUMER_SOCIAL_CAPITAL)
            consumer.save()
