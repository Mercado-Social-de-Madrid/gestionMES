import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Account, Consumer
from currency.models import GuestAccount
from currency_server.fetch_account_info import fetch_account, fetch_guest_account
from intercoop.models import IntercoopAccount, IntercoopEntity
from mes import settings


class Command(BaseCommand):
    help = 'Transform previous intercoop consumers'
    notfound = []
    fetched = 0


    def handle(self, *args, **options):

        entity = IntercoopEntity.objects.all().first()
        accounts = Consumer.objects.filter(iban_code='ES1400369533204977465526')
        for acc in accounts:
            print(acc)

            intercoop, created = IntercoopAccount.objects.get_or_create(cif=acc.cif, entity=entity)
            intercoop.first_name = acc.first_name
            intercoop.last_name = acc.last_name
            intercoop.contact_phone = acc.contact_phone
            intercoop.contact_email = acc.contact_email
            intercoop.address = acc.address
            intercoop.city = acc.city
            intercoop.province = acc.province
            intercoop.postalcode = acc.postalcode
            intercoop.registration_date = acc.registration_date
            intercoop.validated = True
            intercoop.active = True
            intercoop.entity = entity
            intercoop.save()

            acc.delete()

