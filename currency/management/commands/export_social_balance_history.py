from django.core.management.base import BaseCommand
import csv

from social_balance.models import BalanceProcess
from social_balance.models.balance import EntitySocialBalance
from accounts.models.account import Entity, Provider, Colaborator


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


def get_sponsor_last_year(entity, year):
    last_process = BalanceProcess.objects.filter(account=entity, year=year).first()
    if last_process:
        sponsor = last_process.sponsor.first_name + " " + last_process.sponsor.last_name
    else:
        sponsor = ""
    return sponsor


def get_type_entity(entity):
    if isinstance(entity, Provider):
        return 'Proveedora'
    elif isinstance(entity, Colaborator):
        if entity.is_sponsor:
            return "Patrocinadora"
        elif entity.is_collaborator:
            return "Colaboradora"

    return ""


class Command(BaseCommand):
    help = 'Export list of entities with social balace status of last years'

    def add_arguments(self, parser):

        parser.add_argument('year_start', type=int, help='Year start')
        parser.add_argument('year_end', type=int, help='Year end')

    def handle(self, *args, **options):

        year_start = options['year_start']
        year_end = options['year_end']

        years = list(range(year_start, year_end + 1))

        headers = ['Nombre', 'Email', 'Telefono', 'Tipo', 'Año de constitución',
                   'Fecha de alta MES', 'Madrina ultimo año'] + years
        data = []

        entities = Entity.objects.active()

        print(f'Active entities: {len(entities)}')

        for entity in entities:
            name = entity.name
            email = entity.contact_email
            phone = entity.contact_phone
            start_year = entity.start_year
            registration_date = str(entity.registration_date)

            sponsor = get_sponsor_last_year(entity, years[len(years) - 1])
            entity_type = get_type_entity(entity)

            sb = get_social_balance_statuses(entity, years)

            data.append([name, email, phone, entity_type, start_year, registration_date, sponsor] + sb)

        with open('balances_sociales.csv', 'w') as f:
            write = csv.writer(f, delimiter=';')
            write.writerow(headers)
            write.writerows(data)

        print("Exported")


