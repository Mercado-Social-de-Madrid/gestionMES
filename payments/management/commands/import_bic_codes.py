import csv
import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Entity, Account
from mes import settings
from payments.models import BankBICCode
from social_balance.models import EntitySocialBalance


class Command(BaseCommand):
    help = 'Import BIC codes from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='Indicates the CSV file to import fields from')

    def handle(self, *args, **options):

        csvfile = options['csvfile']

        with open(csvfile, 'r'  ) as fp:
            csv_reader = csv.reader(fp, delimiter=';')

            for row in csv_reader:
                bic, created = BankBICCode.objects.get_or_create(bank_code=row[0])
                bic.bank_name = row[1]
                bic.bic_code = row[2]
                bic.save()
