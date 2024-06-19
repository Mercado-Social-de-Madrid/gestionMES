
from django.core.management.base import BaseCommand

from accounts.models import Account
from intercoop.models import IntercoopAccount


class Command(BaseCommand):
    help = 'Generate initial member ids'

    def handle(self, *args, **options):

        print("Socias comunes")
        print("==========================")

        accounts = Account.objects.all()
        for account in accounts:
            if not account.member_id:
                new_member_id = Account.get_new_member_id()
                account.member_id = new_member_id
                account.save()

                print('"member_id":"{}", "cif":"{}"'.format(new_member_id, account.cif))

        print("\nSocias de intercooperación")
        print("==========================")

        intercoop = IntercoopAccount.objects.all()
        for account in intercoop:
            if not account.member_id:
                new_member_id = IntercoopAccount.get_new_member_id()
                account.member_id = new_member_id
                account.save()

                print('"member_id":"{}", "cif":"{}"'.format(new_member_id, account.cif))