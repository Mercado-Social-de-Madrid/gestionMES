import csv
import json
import re

import requests
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from accounts.models import Provider, TERR_LOCAL, TERR_COUNTRY, LegalForm, Entity
from mes import settings
from social_balance.models import EntitySocialBalance, SocialBalanceBadge
from social_balance.renderer import BadgeRenderer


class Command(BaseCommand):
    help = 'Generate social badges for a year'

    def add_arguments(self, parser):
        parser.add_argument('year', type=str, help='Social balance year')

    def handle(self, *args, **options):

        year = options['year']
        badge = SocialBalanceBadge.objects.get(year=year)

        renderer = BadgeRenderer(badge)
        renderer.configure_webdriver()

        entities = Entity.objects.filter(social_balances__isnull=False).distinct()
        for entity in entities:
            balance = EntitySocialBalance.objects.filter(entity=entity, year=year)
            if not balance.exists():
                print('{}: No balance. Passing...'.format(entity.display_name))
                continue

            balance = balance.first()
            renderer.update_balance_image(balance)

