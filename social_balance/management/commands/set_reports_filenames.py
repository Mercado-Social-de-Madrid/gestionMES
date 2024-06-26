import os

from django.core.management.base import BaseCommand

from social_balance.models import EntitySocialBalance


class Command(BaseCommand):
    help = 'Fill report filenames field to ensure all reports have all the same name and download url'

    def add_arguments(self, parser):

        parser.add_argument('year', type=int, help='Year')

    def handle(self, *args, **options):

        year = options['year']

        social_balances = EntitySocialBalance.objects.filter(year=year)
        for social_balance in social_balances:
            if social_balance.report:
                social_balance.entity.report_filename = os.path.basename(social_balance.report.name)
                social_balance.entity.save()

