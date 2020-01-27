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
    help = 'Creates the currency purchase transaction in the currency server (for cases it failed)'

    def add_arguments(self, parser):

        parser.add_argument('cif', type=str, help='Account CIF')
        parser.add_argument('amount', type=int, help='amount in euros of the purchase')


    def handle(self, *args, **options):

        cif = options['cif']
        amount = options['amount']

        account = Account.objects.get(cif=cif)
        success, uuid = wallet_transaction.add_transaction(
            account=account,
            amount=float(amount),
            concept='Compra de etics')

        print(success)