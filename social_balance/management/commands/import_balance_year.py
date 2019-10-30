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
        parser.add_argument('csvfile', type=str, help='Indicates the CSV file to import balance history from')
        parser.add_argument('year', type=str, help='Indicates the CSV file to import balance history from')

    def handle(self, *args, **options):

        csvfile = options['csvfile']
        year = options['year']

        with open(csvfile, 'r', encoding="utf8") as fp:
            csv_reader = csv.reader(fp, delimiter=';')
            line = 0

            for row in csv_reader:
                if line == 0:
                    line += 1
                    continue

                entity_name = row[0]
                cif = row[1]

                if cif is None or cif is '':
                    print("{} no tiene CIF".format(entity_name))
                    continue

                entity = Entity.objects.filter(cif=cif)
                if not entity.exists():
                    print("{}({}) no existe.".format(entity_name, cif))
                    continue

                entity = entity.first()

                balance, created = EntitySocialBalance.objects.get_or_create(entity=entity, year=year)
                balance.done = True
                balance.achievement = row[4]
                balance.challenge = row[5]
                balance.save()




