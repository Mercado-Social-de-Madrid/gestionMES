import json
import re
import urllib.request

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Consumer
from mes import settings


class Command(BaseCommand):
    help = 'Fetch current status of every user in the system from the external source'



    def handle(self, *args, **options):

        for entity in Provider.objects.all().prefetch_related('social_balances'):
            balance = entity.social_balances.all().first()
            if balance and balance.done:
                print(balance.external_id)

                report = 'https://madrid.mercadosocial.net/balance/balances_2018/{}.pdf'.format(balance.external_id)
                image = 'https://madrid.mercadosocial.net/balance/img/entidades/{}.jpg'.format(balance.external_id)

                try:
                    reportFile = urllib.request.urlopen(report)
                    with open('{}.pdf'.format(balance.external_id), 'wb') as output:
                        output.write(reportFile.read())
                except Exception as e:
                    print(e)

                try:
                    imageFile = urllib.request.urlopen(image)
                    with open('{}.jpg'.format(balance.external_id), 'wb') as output:
                        output.write(imageFile.read())
                except Exception as e:
                    print(e)