from django.core.management.base import BaseCommand

from helpers.url import remove_special_chars
from social_balance.models import EntitySocialBalance


class Command(BaseCommand):
    help = ('Check balance report path Entities and optionally fix it. '
            '¡IMPORTANT! to fix reports names, comment temporarily last line in set_report_filename presave function.'
            'After command execution, uncomment it again')

    def add_arguments(self, parser):

        parser.add_argument('--year', type=int, help='Balance year')
        parser.add_argument('--fix', type=bool, nargs='?', default=False)


    def handle(self, *args, **options):

        fix = options['fix']

        year_balance = options['year']
        balances = EntitySocialBalance.objects.filter(year=year_balance)

        reserved_chars = "!*'();:@&=+$,/?#[]"

        for balance in balances:
            if balance.report:
                if not balance.report.name.startswith("reports/"):
                    print('{}. Wrong report name. {}. Id {}'.format(balance.entity.name, balance.report.name, balance.id))

                    if fix:
                        print('Fixing reports/ path...')
                        balance.entity.report_filename = balance.report.name
                        balance.entity.save()
                        fixed_name = 'reports/' + balance.report.name
                        balance.report.name = fixed_name
                        balance.save()

                original_name = balance.report.name.replace("reports/", "")
                for char in reserved_chars:
                    if char in original_name:
                        print('{}. Invalid URL char: {}. {}. Id {}'.format(
                            balance.entity.name, char, balance.report.name, balance.id))

                        if fix:
                            print('Fixing reserved char...')
                            cleaned_url = remove_special_chars(original_name)
                            balance.entity.report_filename = cleaned_url
                            balance.entity.save()
                            balance.report.name = 'reports/' + cleaned_url
                            balance.save()




