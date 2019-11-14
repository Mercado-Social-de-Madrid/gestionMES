import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, OPTED_OUT
from mes import settings


class Command(BaseCommand):
    help = 'Fetch current status of every user in the system from the external source'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to import providers from')



    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        models = []
        with open(jsonfile, 'rb') as fp:
            accounts = json.load(fp)

            for account in accounts:

                provider = Provider()
                provider.cif = account['cif']
                provider.name = account['full_name']
                provider.short_description = account['short_description'] if 'short_description' in account else ''
                provider.description = provider.short_description
                if 'legal_name' in account:
                    provider.business_name = account['legal_name']
                provider.territory = TERR_COUNTRY if 'territory' in account and account['territory']=='Estatal' else TERR_LOCAL
                provider.member_type = settings.MEMBER_PROV
                provider.address = account['address']

                if 'city' in account:
                    provider.city = account['city']
                if 'province' in account:
                    provider.province = account['province']

                if 'legal_form' in account:
                    legal = LegalForm.objects.filter(title=account['legal_form'])
                    if legal.exists():
                        provider.legal_form = legal.first()
                    else:
                        print(account['legal_form'])

                if 'conditions' in account:
                    provider.payment_conditions = account['conditions']

                if 'start_year' in account:
                    provider.start_year = int(account['start_year'])

                if 'webpage' in account:
                    provider.webpage_link = account['webpage']
                provider.contact_email = account['contact_email']
                if 'contact_phone' in account:
                    provider.contact_phone = account['contact_phone']

                if 'zipcode' in account:
                    provider.postalcode = account['zipcode']

                if 'max_accepted' in account:
                   provider.max_percent_payment = float(account['max_accepted'].replace(',','.'))

                if 'bonus_percent_entity' in account:
                    provider.bonus_percent_entity = float(account['bonus_percent_entity'].replace(',','.'))

                if 'bonus_percent_general' in account:
                    provider.bonus_percent_general = float(account['bonus_percent_general'].replace(',', '.'))

                if 'username' in account:
                    provider.cyclos_user = account['username']

                if 'social' in account:
                    sociallinks = account['social']
                    links =  re.findall(r'(https?://[^\s]+)', sociallinks)
                    for link in links:
                        if 'facebook.com' in link:
                            provider.facebook_link = link
                        if 'twitter.com' in link:
                            provider.twitter_link = link
                        if 'telegram.me' in link:
                            provider.telegram_link = link
                        if 'instagram.com' in link:
                            provider.instagram_link = link

                    twitter = re.findall(r'[Tt]witter\s*:?\s*@(\w+)\.?', sociallinks)
                    for twit in twitter:
                        provider.twitter_link = 'https://twitter.com/{}'.format(twit)

                    instagram = re.findall(r'[Ii]nstagram\s*:?\s*@(\w+)\.?', sociallinks)
                    for inst in instagram:
                        provider.instagram_link = 'https://instagram.com/{}'.format(inst)

                if 'registration_date' in account:
                    provider.registration_date = account['registration_date']

                if 'opted_out_date' in account:
                    provider.opted_out_date = account['opted_out_date']

                if 'opted_out' in account and account['opted_out'] == True:
                    provider.status = OPTED_OUT

                print('saving {}'.format(provider.cif))
                try:
                    provider.save()
                except IntegrityError as e:
                    print (e)
                except Exception as e:
                    print (e)
