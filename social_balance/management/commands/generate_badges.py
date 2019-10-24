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


class Command(BaseCommand):
    help = 'Generate social badges for a year'

    def add_arguments(self, parser):
        parser.add_argument('year', type=str, help='Social balance year')

    def handle(self, *args, **options):

        year = options['year']
        badge = SocialBalanceBadge.objects.get(year=year)

        weboptions = webdriver.ChromeOptions()
        weboptions.add_argument('headless')
        DRIVER = 'chromedriver'
        driver = webdriver.Chrome(DRIVER, chrome_options=weboptions)
        driver.set_window_position(0, 0)
        driver.set_window_size(1200, 850)

        entities = Entity.objects.filter(social_balances__isnull=False).distinct()
        for entity in entities:
            url = settings.BASESITE_URL + reverse('balance:badge_render', kwargs={'pk':badge.pk }) + '?id=' + str(entity.pk)
            print(entity.display_name)
            driver.get(url)

            img_temp = NamedTemporaryFile()
            png = driver.get_screenshot_as_png()
            img_temp.write(png)
            img_temp.flush()

            balance = EntitySocialBalance.objects.get(entity=entity, year=year)
            balance.badge_image.save(f"{balance.year}_{entity.pk}", File(img_temp))

        driver.quit()

