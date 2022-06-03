# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.functions import ExtractYear
from django.views.generic.base import TemplateView

from accounts.models import Provider, Account, Consumer, OPTED_OUT


class AccountsReportView(TemplateView):

    template_name = 'account/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        years = Account.objects.filter(registration_date__isnull=False).annotate(year=ExtractYear('registration_date')).order_by('year').values_list('year', flat=True).distinct()
        reports = []
        providers = Provider.objects.all()
        opted = Account.objects.filter(status=OPTED_OUT, opted_out_date__isnull=True)
        for year in years:
            provider_signups = Provider.objects.filter(registration_date__year=year)
            consumer_signups = Consumer.objects.filter(registration_date__year=year)
            account_optedout = Account.objects.filter(status=OPTED_OUT, opted_out_date__year=year)
            report = {
                'year':year,
                'provider_signups': provider_signups,
                'consumer_signups': consumer_signups,
                'consumer_signups_count': consumer_signups.count(),
                'provider_signups_count': provider_signups.count(),
                'account_optedout': account_optedout,
                'account_optedout_count': account_optedout.count(),
            }
            report['total_signups'] = report['consumer_signups_count'] + report['provider_signups_count']
            reports.append(report)

        context['report'] = reports

        return context