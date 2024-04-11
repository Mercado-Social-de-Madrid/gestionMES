import requests
import os
from django.core.management.base import BaseCommand

from accounts.models import Entity


class Command(BaseCommand):
    help = 'Check report filename with HA tool (See issue #179)' # Remember to include 'balance_detail' field in HA entities response

    def handle(self, *args, **options):

        r = requests.get('https://app.mercadosocial.net/api/v1/entities/?limit=2000')
        if r.ok:
            result = r.json()['entities']

            entities = Entity.objects.all()
            for entity in entities:
                app_entity = next(filter(lambda x: x["member_id"] == entity.member_id, result), None)
                if app_entity:
                    if app_entity['balance_detail']:
                        filename = os.path.basename(app_entity['balance_detail'])
                        if not entity.report_filename == filename:
                            print(f'Nombres de archivo de balance no coincide: {entity.name} - {entity.cif} - {entity.member_id}\n{entity.report_filename} - {filename}')
                    # else:
                    #     print(f'No existe nombre de archivo en HA: {entity.name} - {entity.cif} - {entity.member_id}')

        else:
            print('Fallo en la petición de entidades a la HA')