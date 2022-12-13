from django.core.management.base import BaseCommand

from accounts.models import Entity
from social_balance.models import EntitySocialBalance, SocialBalanceBadge
from social_balance.renderer import BadgeRenderer


class Command(BaseCommand):
    help = 'Generate social badges for a year'

    def add_arguments(self, parser):
        parser.add_argument('year', type=str, help='Social balance year')

    def handle(self, *args, **options):

        year = options['year']
        badge = SocialBalanceBadge.objects.get(year=year)

        renderer = BadgeRenderer(badge)
        renderer.configure_webdriver()

        entities = Entity.objects.filter(social_balances__isnull=False).distinct()
        for entity in entities:
            balance = EntitySocialBalance.objects.filter(entity=entity, year=year)
            if not balance.exists():
                print('{}: No balance. Passing...'.format(entity.display_name))
                continue

            print('{}: Generating badge...'.format(entity.display_name))
            balance = balance.first()
            renderer.update_balance_image(balance)

