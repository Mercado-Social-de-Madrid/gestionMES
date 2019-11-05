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
    help = 'Solve encoding errors in entities'
    notfound = []
    fetched = 0


    def handle(self, *args, **options):

        providers = Provider.objects.filter(pk=225)
        for prov in providers:
            print(prov.display_name)

            try:
                prov.name = prov.name.encode('latin1').decode('utf8')
            except UnicodeDecodeError:
                pass

            try:
                prov.business_name = prov.business_name.encode('latin1').decode('utf8')
            except UnicodeDecodeError:
                pass

            try:
                prov.short_description = prov.short_description.encode('latin1').decode('utf8')
            except UnicodeDecodeError:
                pass

            try:
                prov.address = prov.address.encode('latin1').decode('utf8')
            except UnicodeDecodeError:
                pass
            prov.save()