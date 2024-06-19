import argparse

from django.core.management.base import BaseCommand

from accounts.models import Account


class Command(BaseCommand):
    help = 'Issue 180'

    def add_arguments(self, parser):
        parser.add_argument('--fix', action='store_true')
        parser.set_defaults(fix=False)

    def handle(self, *args, **options):

        accounts = Account.objects.active()
        print("\nChecking accounts:")

        member_ids = []
        duplicated = 0
        for account in accounts:

            if account.member_id in member_ids:
                print('Duplicated member_id: {}. CIF: {}'.format(account.member_id, account.cif))
                duplicated += 1

                if options['fix']:
                    new_member_id = Account.get_new_member_id()
                    print('Fixing... New member id: {}'.format(new_member_id))
                    account.member_id = new_member_id
                    account.save()

            else:
                member_ids.append(account.member_id)

        print('{} duplicated accounts'.format(duplicated))
