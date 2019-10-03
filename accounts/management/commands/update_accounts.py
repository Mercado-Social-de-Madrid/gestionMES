import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Account
from currency.models import GuestAccount
from currency_server.fetch_account_info import fetch_account, fetch_guest_account
from mes import settings


class Command(BaseCommand):
    help = 'Fetch current status of every user in the system from the external source'
    notfound = []
    fetched = 0

    def fetch_accounts(self):
        accounts = Account.objects.all()
        for account in accounts:
            result = fetch_account(account)
            if result is True:
                print('{}: updated succesfully'.format(account))
            elif result is False:
                self.notfound.append(account)
                print('{}: failed'.format(account))
            else:
                self.notfound.append(account)
                print('{} not fetched: {}'.format(account, result))

        self.fetched += accounts.count()


    def fetch_guests(self):
        guests = GuestAccount.objects.all()
        for guest in guests:
            result = fetch_guest_account(guest)
            if result is True:
                print('{}: updated succesfully'.format(guest))
            elif result is False:
                self.notfound.append(guest)
                print('{}: failed'.format(guest))
            else:
                self.notfound.append(guest)
                print('{} not fetched: {}'.format(guest, result))

        self.fetched += guests.count()

    def handle(self, *args, **options):
        self.fetch_accounts()
        self.fetch_guests()

        print('Completed fetching info from {} accounts! Missing {} accounts'.format(self.fetched, len(self.notfound)) )
        for account in self.notfound:
            print(account)