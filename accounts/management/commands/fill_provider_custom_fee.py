
from django.core.management.base import BaseCommand
from accounts.models import Provider
from payments.models import FeeRange


class Command(BaseCommand):
    help = 'Fill Provider custom_fee field with FeeRange calculator'

    def handle(self, *args, **options):
        providers = Provider.objects.all()
        for prov in providers:
            prov.custom_fee = FeeRange.calculate_provider_fee(prov)
            prov.save()
