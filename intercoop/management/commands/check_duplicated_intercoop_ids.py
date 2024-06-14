from django.core.management.base import BaseCommand

from intercoop.models import IntercoopAccount


class Command(BaseCommand):
    help = 'Issue 180'

    def handle(self, *args, **options):

        accounts = IntercoopAccount.objects.all()
        print("\nChecking accounts:")

        member_ids = []
        duplicated = 0
        for account in accounts:

            if account.member_id in member_ids:
                print('Duplicated member_id: {}. CIF: {}'.format(account.member_id, account.cif))
                new_member_id = IntercoopAccount.get_new_member_id()
                print('New member id: {}'.format(new_member_id))
                account.member_id = new_member_id
                account.save()

                duplicated += 1
            else:
                member_ids.append(account.member_id)

        print('{} duplicated accounts'.format(duplicated))
