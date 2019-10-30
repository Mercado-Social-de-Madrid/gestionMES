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

    def handle(self, *args, **options):

        csvfile = options['csvfile']

        with open(csvfile, 'r', encoding="utf8") as fp:
            csv_reader = csv.reader(fp, delimiter=';')
            years = []
            line = 0

            for row in csv_reader:
                if line == 0:
                    years = row[2:]
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

                for col, year in enumerate(years):
                    result = row[col+2].lower()
                    if 'exent' in result:
                        print('{} - {}: Exenta!'.format(entity.display_name, year))
                        balance, created = EntitySocialBalance.objects.get_or_create(entity=entity, year=year)
                        balance.is_exempt = True
                        balance.save()

                    elif 'no hech' in result:
                        print('{} - {}: No hecho!'.format(entity.display_name, year))
                        balance, created = EntitySocialBalance.objects.get_or_create(entity=entity, year=year)
                        balance.done = False
                        balance.save()

                    elif 'hech' in result:
                        print('{} - {}: hecho!'.format(entity.display_name, year))
                        balance, created = EntitySocialBalance.objects.get_or_create(entity=entity, year=year)
                        balance.done = True
                        balance.save()

                    #print('{}:{}'.format(year, row[col+2].lower()))

                    pass
                    '''balance, created = EntitySocialBalance.objects.get_or_create(entity=entity.first(), year=year)
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

                    balance.save()'''



