import json

from django.core.management.base import BaseCommand

from accounts.models import Entity, Account, Provider


class Command(BaseCommand):
    help = 'Export url of balance report of Providers'

    def add_arguments(self, parser):

        parser.add_argument('year', type=int, help='Balance year')
        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to export data')


    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        year_balance = options['year']
        providers = Provider.objects.filter(social_balances__year=year_balance)

        data = []
        for provider in providers:

            report = provider.social_balances.get(year=year_balance).report

            data.append({
                'name': provider.display_name,
                'member_id': provider.member_id,
                'cif': provider.cif,
                'balance_report': report.name if report else None,
            })

        with open(jsonfile, 'w') as f:
            json_entities = json.dumps(data)
            f.write(json_entities)
            f.close()

