import csv
import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Entity
from mes import settings
from social_balance.models import EntitySocialBalance


class Command(BaseCommand):
    help = 'Import social balances reports info from an external source'

    def add_arguments(self, parser):

        parser.add_argument('csvfile', type=str, help='Indicates the CSV file to import balances from')
        parser.add_argument('year', type=int, help='Indicates the CSV year')

    def handle(self, *args, **options):

        csvfile = options['csvfile']
        year = options['year']


        with open(csvfile, 'r') as fp:
            csv_reader = csv.reader(fp, delimiter=';')
            line = 0
            for row in csv_reader:
                if line == 0:
                    line += 1
                    continue

                cyclos_user = row[1]
                if not cyclos_user or cyclos_user == '':
                    continue

                entity = Entity.objects.filter(cyclos_user=cyclos_user)
                if entity.exists():
                    balance, created = EntitySocialBalance.objects.get_or_create(entity=entity.first(), year=year)
                    balance.external_id = row[0]
                    if row[3] == 'Exenta':
                        balance.is_exempt = True
                    elif row[3] == 'Hecho':
                        balance.is_exempt = False
                        balance.done = True
                        balance.is_public = row[4] == 'x'
                    else:
                        balance.done = False
                        balance.is_exempt = False

                    balance.save()

                else:
                    print "{} does not exist.".format(cyclos_user)

