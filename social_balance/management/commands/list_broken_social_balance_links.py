import logging

from django.core.mail import mail_admins
from django.core.management import BaseCommand
from django.http import HttpResponse

from social_balance.models import EntitySocialBalance

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'List broken social balance links'

    def handle(self, *args, **options):
        social_balances = EntitySocialBalance.objects.filter(report__isnull=False)
        affected_reports = ''
        logger.info('Affected social balance reports:')
        for balance in social_balances:
            if balance.report.name:
                filename = balance.report.name.split('/')[-1]
                try:
                    response = HttpResponse(balance.report, content_type='application/pdf')
                    response['Content-Disposition'] = 'attachment; filename=%s' % filename
                except FileNotFoundError:
                    url_split = balance.report.url.split('/')
                    if url_split[2] != 'reports':
                        entity_info = f'- {balance.entity.name}, {balance.year}, {balance.report.name}\n'
                        affected_reports += entity_info
                        logger.info(entity_info)
                except PermissionError:
                    pass
        print(affected_reports)
        if affected_reports:
            self.send_email(affected_reports)

    def send_email(self, affected_reports):
        subject = 'ERROR - Hay enlaces rotos en las infografías de las siguientes entidades:'
        mail_admins(
            subject=subject,
            message=affected_reports,
            fail_silently=True,
        )
        logger.info('Email sent to admins.')



