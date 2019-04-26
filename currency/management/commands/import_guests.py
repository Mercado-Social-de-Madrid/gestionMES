import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Consumer, Account
from currency.models import GuestAccount
from mes import settings


class Command(BaseCommand):
    help = 'Fetch current status of every user in the system from the external source'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to import guests from')


    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        with open(jsonfile, 'r') as fp:
            accounts = json.load(fp)

            for account in accounts:

                guest = GuestAccount()

                if 'cif' in account:
                    already_user = Account.objects.filter(cif=account['cif']).exists()
                    if already_user:
                        print '{} exists already!'.format(account['cif'])
                    else:
                        guest.cif = account['cif']

                name = account['name'].split(' ')
                guest.first_name = name.pop(0)
                guest.last_name = ' '.join(name)
                if 'address' in account:
                    guest.address = account['address']
                if 'city' in account:
                    guest.city = account['city']
                if 'province' in account:
                    guest.province = account['province']

                if 'legal_form' in account:
                    legal = LegalForm.objects.filter(title=account['legal_form'])
                    if legal.exists():
                        guest.legal_form = legal.first()
                    else:
                        print account['legal_form']

                guest.contact_email = account['email']
                if 'phone' in account:
                    guest.contact_phone = account['phone']

                if 'zipcode' in account:
                    guest.postalcode = account['zipcode']

                if 'cyclos_user' in account:
                    guest.cyclos_user = account['cyclos_user']


                print 'saving {}'.format(guest)
                try:
                    guest.save()
                except IntegrityError as e:
                    print e
                except Exception as e:
                    print e

