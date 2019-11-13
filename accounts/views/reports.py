# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.conf import settings
from django.db.models import Prefetch
from django.db.models.functions import ExtractYear
from django.utils.translation import gettext as _
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.models import Provider, ACTIVE, Account, Consumer
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.XFrameExemptMixin import XFrameOptionsExemptMixin
from social_balance.models import EntitySocialBalance, SocialBalanceBadge



class AccountsReportView(TemplateView):

    template_name = 'account/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        years = Account.objects.filter(registration_date__isnull=False).annotate(year=ExtractYear('registration_date')).order_by('year').values_list('year', flat=True).distinct()
        print (years)
        reports = []
        providers = Provider.objects.all()
        for year in years:
            provider_signups = Provider.objects.filter(registration_date__year=year)
            consumer_signups = Consumer.objects.filter(registration_date__year=year)
            report = {
                'year':year,
                'provider_signups': provider_signups,
                'consumer_signups': consumer_signups,
                'consumer_signups_count': consumer_signups.count(),
                'provider_signups_count': provider_signups.count()
            }
            report['total_signups'] = report['consumer_signups_count'] + report['provider_signups_count']
            reports.append(report)

        context['report'] = reports

        return context