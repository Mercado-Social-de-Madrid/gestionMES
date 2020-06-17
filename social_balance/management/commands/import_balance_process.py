import csv
import json
import re

import requests
from datetime import date, datetime
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Entity
from core.models import User
from mes import settings
from social_balance.models import EntitySocialBalance, BalanceProcess, BALANCE_SHORT, BALANCE_LONG, BALANCE_EXEMPT

COL_NAME = 0
COL_COMMENT = 1
COL_CIF = 2
COL_SPONSOR = 3
COL_STATUS = 4
COL_TYPE = 8

BALANCE_TYPE_DICT = {
    'BS acotado':BALANCE_SHORT,
    'BS largo':BALANCE_LONG,
    'exenta':BALANCE_EXEMPT
}
BALANCE_STATUS_DICT = {
    'No se han registrado':2,
    'Se han registrado-email con clave': 3,
    'Abierto': 4,
    'Cerrado': 5,
}

class Command(BaseCommand):
    help = 'Import social balance processes from an external source'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='Indicates the CSV file to import balance history from')
        parser.add_argument('year', type=str, help='Indicates the balance year the process belong to')

    def handle(self, *args, **options):

        csvfile = options['csvfile']
        year = options['year']
        start_date = datetime(2020,4,27)
        date_regex = re.compile('^([0-9][0-9]/[0-9][0-9]/2020)')

        with open(csvfile, 'r', encoding="utf8") as fp:
            csv_reader = csv.reader(fp, delimiter=';')

            for row in csv_reader:

                entity_name = row[COL_NAME]
                cif = row[COL_CIF]

                if cif is None or cif is '':
                    print("{} no tiene CIF".format(entity_name))
                    continue

                entity = Entity.objects.filter(cif=cif)
                if not entity.exists():
                    print("{}({}) no existe.".format(entity_name, cif))
                    continue

                entity = entity.first()
                sponsor = row[COL_SPONSOR]
                bal_type = row[COL_TYPE]
                if bal_type in BALANCE_TYPE_DICT:
                    bal_type = BALANCE_TYPE_DICT[bal_type]


                process = BalanceProcess.objects.create_process(account=entity, year=year)
                process.workflow.start_time = start_date
                if bal_type == BALANCE_EXEMPT:
                    last = process.workflow.get_last_step()
                    process.workflow.current_state = last

                user = User.objects.filter(username=sponsor).first()
                if user:
                    process.sponsor = user
                    status = row[COL_STATUS]
                    if status in BALANCE_STATUS_DICT:
                        step = BALANCE_STATUS_DICT[status]
                        current_step = process.workflow.get_step(step)
                        process.workflow.current_state = current_step

                process.balance_type = bal_type
                process.workflow.save()
                process.save()

                sp_comment = row[COL_COMMENT]
                if sp_comment and sp_comment != '':
                    process.workflow.add_comment(None, sp_comment, start_date)

                comments = row[COL_TYPE+1:]
                for comment in comments:
                    if comment and comment != '':
                        timestamp = None
                        hasdate = re.match(date_regex, comment)
                        if hasdate:
                            strdate = hasdate.group(1)
                            timestamp = datetime.strptime(strdate, '%d/%m/%Y')
                            comment = re.sub(date_regex, '', comment)
                        process.workflow.add_comment(None, comment, timestamp)

