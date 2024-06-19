
from django.core.management.base import BaseCommand

from accounts.models import Account
from intercoop.models import IntercoopAccount


class Command(BaseCommand):
    help = 'Generate initial member ids'

    def handle(self, *args, **options):

        print("Socias comunes")
        print("==========================")

        accounts = Account.objects.all()

        print("Eliminando números de socia anteriores")
        for account in accounts:
            account.member_id = None
            account.save()

        for account in accounts:
            new_member_id = Account.get_new_member_id()
            account.member_id = new_member_id
            account.save()

            print('"member_id":"{}", "cif":"{}"'.format(new_member_id, account.cif))


        print("\nSocias de intercooperación")
        print("==========================")

        intercoop = IntercoopAccount.objects.all()

        print("Eliminando números de socia anteriores")
        for account in intercoop:
            account.member_id = None
            account.save()

        for account in intercoop:
            new_member_id = IntercoopAccount.get_new_member_id()
            account.member_id = new_member_id
            account.save()

            print('"member_id":"{}", "cif":"{}"'.format(new_member_id, account.cif))