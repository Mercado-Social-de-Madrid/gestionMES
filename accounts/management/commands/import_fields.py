import csv
import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Entity, Account
from mes import settings
from social_balance.models import EntitySocialBalance


class Command(BaseCommand):
    help = 'Import fields from CSV (first row defines field names)'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='Indicates the CSV file to import fields from (first column must be cif)')

    def handle(self, *args, **options):

        csvfile = options['csvfile']

        with open(csvfile, 'r', encoding="utf8") as fp:
            csv_reader = csv.reader(fp, delimiter=';')
            fields = []
            line = 0

            for row in csv_reader:
                if line == 0:
                    fields = row[1:]
                    line += 1
                    continue

                cif = row[0]

                if cif is None or cif is '':
                    continue

                account = Account.objects.filter(cif=cif)
                if not account.exists():
                    print("No existe socia con cif {}.".format(cif))
                    continue

                account = account.first()
                updated = False
                for col, field in enumerate(fields):
                    field_value = row[col+1]
                    if field_value not in (None,''):
                        setattr(account, field, field_value)
                        updated = True

                if updated:
                    print('{} updated.'.format(account.display_name))
                    account.save()

