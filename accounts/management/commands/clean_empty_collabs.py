import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.utils import timezone

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Account, EntityCollaboration
from currency.models import GuestAccount
from currency_server.fetch_account_info import fetch_account, fetch_guest_account, fetch_intercoop_account
from intercoop.models import IntercoopAccount
from mes import settings


class Command(BaseCommand):
    help = 'Fetch current status of every user in the system from the external source'
    notfound = []
    fetched = 0

    def add_arguments(self, parser):
        parser.add_argument('cif', type=int, nargs='?', default=None)


    def clean_collabs(self):

        emptyCollabs = EntityCollaboration.objects.filter(entity__isnull=True)
        for empty in emptyCollabs:
            print(empty)
            empty.delete()

    def handle(self, *args, **options):

        self.clean_collabs()

        print('Completed task:' +  str(timezone.now()))
