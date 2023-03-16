
from django.core.management.base import BaseCommand
from accounts.models import Provider, Consumer, SocialCapital, Account
from intercoop.models import IntercoopAccount
from payments.models import FeeRange


class Command(BaseCommand):
    help = 'Generate initial member ids'

    def handle(self, *args, **options):

        print("Socias comunes")
        print("==========================")

        accounts = Account.objects.all().order_by('registration_date')
        for account in accounts:
            new_member_id = Account.get_new_member_id()
            account.member_id = new_member_id
            account.save()

            print ("{} | {} | {}".format(new_member_id, account.cif, account.display_name))

        print("\nSocias de intercooperación")
        print("==========================")

        intercoop = IntercoopAccount.objects.all().order_by('registration_date')
        for account in intercoop:
            new_member_id = IntercoopAccount.get_new_member_id()
            account.member_id = new_member_id
            account.save()

            print("{} | {} | {}".format(new_member_id, account.cif, account.display_name))