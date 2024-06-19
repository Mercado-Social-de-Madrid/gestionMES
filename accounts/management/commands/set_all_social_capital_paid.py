
from django.core.management.base import BaseCommand

from accounts.models import SocialCapital


class Command(BaseCommand):
    help = 'All auto-filled social capitals must be marked as paid (see fill_social_capital.py)'

    def handle(self, *args, **options):
        social_capitals = SocialCapital.objects.all()

        total = len(social_capitals)
        actual = 0

        for social_capital in social_capitals:
            actual += 1
            print(f'Processing {actual} of {total}')
            social_capital.paid = True
            social_capital.save()
