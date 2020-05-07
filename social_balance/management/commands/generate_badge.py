from django.core.management.base import BaseCommand

from accounts.models import Entity
from social_balance.models import EntitySocialBalance, SocialBalanceBadge
from social_balance.renderer import BadgeRenderer


class Command(BaseCommand):
    help = 'Generate social badges for a year'

    def add_arguments(self, parser):
        parser.add_argument('year', type=str, help='Social balance year')
        parser.add_argument('cif', type=str, help='Entity cif')

    def handle(self, *args, **options):

        year = options['year']
        cif = options['cif']
        badge = SocialBalanceBadge.objects.get(year=year)

        renderer = BadgeRenderer(badge)
        renderer.configure_webdriver()

        entity = Entity.objects.filter(cif=cif).first()
        balance = EntitySocialBalance.objects.filter(entity=entity, year=year)
        if not balance.exists():
            print('{}: No balance. Passing...'.format(entity.display_name))
            return

        balance = balance.first()
        renderer.update_balance_image(balance)

