# -*- coding: utf-8 -*-
import csv
import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Entity, Account
from mes import settings
from payments.models import BankBICCode
from social_balance.models import EntitySocialBalance


class Command(BaseCommand):
    help = 'Created to analyze error in Account annual fee charges section'

    def add_arguments(self, parser):
        parser.add_argument('year', type=str, help='Year of annual fee charge')

    def handle(self, *args, **options):

        year = options['year']

        from accounts.models.account import Account
        from payments.models.fee import AccountAnnualFeeCharge, AnnualFeeCharges
        accounts = Account.objects.all()
        for account in accounts:
            afc = AccountAnnualFeeCharge.objects.filter(account=account,
                                                        annual_charge=AnnualFeeCharges.objects.get(year=year),
                                                        collab=None)
            if len(afc) > 1:
                print(f'\n{account} - {len(afc)} cuotas anuales sin acuerdos de colaboración para {year}.  Ids: ')
                for afc_item in afc:
                    print(f'{afc_item.pk}')
