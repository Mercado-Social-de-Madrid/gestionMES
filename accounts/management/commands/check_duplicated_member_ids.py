from django.core.management.base import BaseCommand

from accounts.models import Account


class Command(BaseCommand):
    help = 'Issue 180'

    def handle(self, *args, **options):

        accounts = Account.objects.active()
        print("\nChecking accounts:")

        member_ids = []
        for account in accounts:

            if account.member_id in member_ids:
                print('Duplicated member_id: {}. CIF: {}'.format(account.member_id, account.cif))
            else:
                member_ids.append(account.member_id)
