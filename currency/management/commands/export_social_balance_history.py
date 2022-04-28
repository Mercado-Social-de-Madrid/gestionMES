import json
import datetime
from django.core.management.base import BaseCommand
from wallets.models.transaction import Transaction
import csv
from social_balance.models.balance import EntitySocialBalance
from accounts.models.account import Entity


def get_social_balance_statuses(entity, years):
    statuses = []
    for year in years:
        sb = EntitySocialBalance.objects.filter(entity=entity, year=year).first()
        if sb:
            if sb.done:
                status = 'REALIZADO'
            elif sb.is_exempt:
                status = 'EXENTA'
            else:
                status = 'NO REALIZADO'
            statuses.append(status)
        else:
            statuses.append("")

    return statuses


class Command(BaseCommand):
    help = 'Export list of entities with social balace status of last years'

    def handle(self, *args, **options):

        # --- Configure years:

        year_begin = 2018
        year_end = 2021

        # --------------------

        years = list(range(year_begin, year_end + 1))

        headers = ['Nombre', 'Email', 'Telefono'] + years
        data = []

        entities = Entity.objects.active()

        print(f'Active entities: {len(entities)}')

        for entity in entities:
            name = entity.name
            email = entity.contact_email
            phone = entity.contact_phone

            sb = get_social_balance_statuses(entity, years)

            data.append([name, email, phone] + sb)

        with open('balances_sociales.csv', 'w') as f:
            write = csv.writer(f, delimiter=';')
            write.writerow(headers)
            write.writerows(data)

        print("Exported")


