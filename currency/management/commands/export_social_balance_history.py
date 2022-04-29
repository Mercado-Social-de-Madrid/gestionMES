from django.core.management.base import BaseCommand
import csv
from social_balance.models.balance import EntitySocialBalance
from accounts.models.account import Entity, Provider


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

    def add_arguments(self, parser):

        parser.add_argument('year_start', type=int, help='Year start')
        parser.add_argument('year_end', type=int, help='Year end')

    def handle(self, *args, **options):

        year_start = options['year_start']
        year_end = options['year_end']

        years = list(range(year_start, year_end + 1))

        headers = ['Nombre', 'Email', 'Telefono'] + years
        data = []

        entities = Provider.objects.active()

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


