import os
from django.core.management.base import BaseCommand

from mes.settings import ROOT_DIR
from social_balance.models import EntitySocialBalance
from django.core.files import File

class Command(BaseCommand):
    help = 'Upload infographics to corresponding entity and year'

    def add_arguments(self, parser):
        parser.add_argument('year', type=str, help='Social balance year')

    def handle(self, *args, **options):

        year = options['year']

        infographics_path = os.path.abspath(os.path.join(ROOT_DIR, 'infographics'))

        if not os.path.exists(infographics_path):
            self.stdout.write(self.style.ERROR('La carpeta "infographics" no existe.'))
            return

        infographics = [archivo for archivo in os.listdir(infographics_path) if os.path.isfile(os.path.join(infographics_path, archivo))]
        print(f'infographics count: {len(infographics)}')

        for infographic in infographics:

            cif, extension = os.path.splitext(infographic)

            entitySB = EntitySocialBalance.objects.filter(entity__cif=cif, year=year).first()

            if entitySB:

                print(f'Procesando entidad: {entitySB.entity.name}. CIF: {cif}')

                full_path = os.path.join(infographics_path, infographic)
                file = File(open(full_path, 'rb'))

                entitySB.report = file
                entitySB.save()

                self.stdout.write(self.style.SUCCESS(f'Infografía subida'))
            else:
                self.stdout.write(self.style.WARNING(f'No se encontró ninguna Entidad con CIF {cif}'))

        self.stdout.write(self.style.SUCCESS('Proceso completado.'))
