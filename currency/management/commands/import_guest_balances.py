import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Consumer, Account
from currency.models import GuestAccount
from currency_server import wallet_transaction
from mes import settings


class Command(BaseCommand):
    help = 'Fetch current status of every user in the system from the external source'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to import guests from')


    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        failed = []
        missing = []
        successes = []

        with open(jsonfile, 'r') as fp:
            accounts = json.load(fp)

            for account in accounts:
                added = False
                accountuser = GuestAccount.objects.filter(cyclos_user=account['cyclos_user']).first()
                if accountuser:

                    if 'balance' in account and float(account['balance']) == 0:
                        added = True
                    else:
                        success, uuid = wallet_transaction.add_transaction(
                            account=accountuser,
                            amount=float(account['balance']),
                            concept='Ajuste de saldo de Boniatos')

                        if success:
                            account['tr'] = uuid
                            successes.append(account)
                            added = True
                        else:
                            account['cause'] = uuid
                            added = True  # to not count it as missing
                            failed.append(account)

                if not added:
                    missing.append(account)

        print 'Process completed!'

        print '{} missing:'.format(len(missing))
        for consumer in missing:
            print consumer
        print '---------------------------------'
        print '{} fails:'.format(len(failed))
        for consumer in failed:
            print consumer

        print '---------------------------------'
        print '{} successes:'.format(len(successes))
        for consumer in successes:
            print consumer
