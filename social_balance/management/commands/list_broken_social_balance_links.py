from django.core.management import BaseCommand
from django.http import HttpResponse

from social_balance.models import EntitySocialBalance


class Command(BaseCommand):
    help = 'List broken social balance links'

    def handle(self, *args, **options):
        social_balances = EntitySocialBalance.objects.filter(report__isnull=False)
        print('Affected social balance reports:')
        for balance in social_balances:
            if balance.report.name:
                filename = balance.report.name.split('/')[-1]
                try:
                    response = HttpResponse(balance.report, content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=%s' % filename
                except FileNotFoundError:
                    url_split = balance.report.url.split('/')
                    if url_split[2] != 'reports':
                        print(f'- {balance.entity.name}, {balance.year}, {balance.report.name}')





