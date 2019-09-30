import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError


from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Consumer, ACTIVE
from currency_server import create_account
from mes import settings


class Command(BaseCommand):
    help = 'Create account in currency server for every user that is missing one'

    def handle(self, *args, **options):

        providers = Provider.objects.filter(status=ACTIVE, app_user__isnull=True)
        failed = []
        for provider in providers:
            try:
                create_account.post_entity(provider)
            except:
                print('{}: Failed!'.format(provider))
                failed.append(provider)


        print('Process completed!')
        print('{} fails'.format(len(failed)))
        for consumer in failed:
            print(consumer)