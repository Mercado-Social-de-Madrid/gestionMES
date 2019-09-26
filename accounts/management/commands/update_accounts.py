import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Account
from currency_server.fetch_account_info import fetch_account
from mes import settings


class Command(BaseCommand):
    help = 'Fetch current status of every user in the system from the external source'



    def handle(self, *args, **options):
        accounts = Account.objects.all()
        notfound = []
        for account in accounts:
            result = fetch_account(account)
            if result is True:
                print('{}: updated succesfully'.format(account))
            elif result is False:
                notfound.append(account)
                print('{}: failed'.format(account))
            else:
                notfound.append(account)
                print('{} not fetched: {}'.format(account, result))

        print('Completed fetching info from {} accounts! Missing {} accounts'.format(accounts.count(), len(notfound)) )
        for account in notfound:
            print account