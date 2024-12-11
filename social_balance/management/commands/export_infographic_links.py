import csv
import os

from django.core.management.base import BaseCommand

from mes.settings import ROOT_DIR, MEDIA_URL
from mes.settings_secret import BASESITE_URL
from social_balance.models.balance import EntitySocialBalance


class Command(BaseCommand):
    help = 'Export social balances infographic links and emails for year passed by argument'

    def add_arguments(self, parser):

        parser.add_argument('year', type=int, help='Year')

    def handle(self, *args, **options):

        year = options['year']

        headers = ['Nombre', 'Email', 'CIF', 'Link infografía', 'Público']
        data = []

        entitiesSB = EntitySocialBalance.objects.filter(year=year)

        for entitySB in entitiesSB:

            if not entitySB.report.name:
                continue

            name = entitySB.entity.name
            email = entitySB.entity.contact_email
            cif = entitySB.entity.cif
            link = BASESITE_URL + MEDIA_URL + entitySB.report.name
            is_public = entitySB.is_public
            data.append([name, email, cif, link, is_public])


        export_path = os.path.abspath(os.path.join(ROOT_DIR, 'export'))
        full_path = os.path.join(export_path, f'balance_social_{year}_links_emails.csv')
        with open(full_path, 'w') as f:
            write = csv.writer(f, delimiter=';')
            write.writerow(headers)
            write.writerows(data)

        print("Exported")


