import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Account, OPTED_OUT, DeletionProcess
from currency.models import GuestAccount
from currency_server.fetch_account_info import fetch_account, fetch_guest_account, fetch_intercoop_account
from intercoop.models import IntercoopAccount
from mes import settings


class Command(BaseCommand):
    help = 'Update opted out dates'
    notfound = []
    fetched = 0


    def handle(self, *args, **options):

        updated = 0
        unknown = Account.objects.filter(status=OPTED_OUT, opted_out_date__isnull=True)
        for account in unknown:
            deletion = DeletionProcess.objects.filter(account=account, cancelled=False, workflow__completed=True).first()
            if deletion:
                account.opted_out_date = deletion.last_update
                account.save()
                updated += 1
            else:
                print(account.display_name)


        print('{} unknown, {} updated.'.format(unknown.count(), updated))
