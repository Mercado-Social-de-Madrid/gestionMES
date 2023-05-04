import json

from django.core.management.base import BaseCommand

from accounts.models import Entity, Account


class Command(BaseCommand):
    help = 'Export member ids of all accounts to a json file'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to export data')


    def list_categories(entity):
        entity.cate


    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        accounts = Account.objects.all()

        data = []
        for account in accounts:

            data.append({
                'name': account.display_name,
                'cif': account.cif,
                'member_id': account.member_id,
            })

        json_data = {
            'accounts': data
        }
        with open(jsonfile, 'w') as f:
            json_entities = json.dumps(json_data)
            f.write(json_entities)
            f.close()

