import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Consumer
from mes import settings


class Command(BaseCommand):
    help = 'Fetch current status of every user in the system from the external source'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to import providers from')



    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        with open(jsonfile, 'r') as fp:
            accounts = json.load(fp)

            for account in accounts:

                consumer = Consumer()
                if not 'cif' in account:
                    print(account['full_name'])
                    print('CIF missing!')
                    continue

                consumer.cif = account['cif']
                name = account['full_name'].split(' ')
                consumer.first_name = name.pop(0)
                consumer.last_name = ' '.join(name)
                consumer.member_type = settings.MEMBER_CONSUMER
                if 'address' in account:
                    consumer.address = account['address']
                    consumer.city = account['city']
                if 'province' in account:
                   consumer.province = account['province']

                if 'legal_form' in account:
                    legal = LegalForm.objects.filter(title=account['legal_form'])
                    if legal.exists():
                        consumer.legal_form = legal.first()
                    else:
                        print(account['legal_form'])

                consumer.contact_email = account['contact_email']
                if 'contact_phone' in account:
                    consumer.contact_phone = account['contact_phone']

                if 'zipcode' in account:
                    consumer.postalcode = account['zipcode']

                if 'username' in account:
                    consumer.cyclos_user = account['username']


                print('saving {}'.format(consumer.cif))
                try:
                    consumer.save()
                except IntegrityError as e:
                    print(e)
                except Exception as e:
                    print(e)

