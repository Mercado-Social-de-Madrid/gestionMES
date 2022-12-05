import os

from django.core.management.base import BaseCommand

from social_balance.models import EntitySocialBalance


class Command(BaseCommand):
    help = 'Fill report filenames field to ensure all reports have all the same name and download url'

    def handle(self, *args, **options):

        social_balances = EntitySocialBalance.objects.filter(year=2020)
        for social_balance in social_balances:
            if social_balance.report:
                # social_balance.report.name = "reports/" + social_balance.report.name
                social_balance.report_filename = os.path.basename(social_balance.report.name)
                social_balance.save()

