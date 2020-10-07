# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, FormView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.models import Entity, ACTIVE
from accounts.views import ProviderFilter
from core.mixins.AjaxFormResponseMixin import AjaxFormResponseMixin
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from social_balance.forms.entity_year import EntityYearBalanceForm
from social_balance.models import SocialBalanceBadge, EntitySocialBalance
from social_balance.forms.bulk_import import ImportSocialBalanceForm

class SocialBalanceYear(PermissionRequiredMixin, FilterView, FilterMixin, ExportAsCSVMixin, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'social_balance.mespermission_can_view_social_balances'
    template_name = 'balance/year/list.html'
    ajax_template_name = 'balance/year/query.html'
    model = Entity
    queryset = Entity.objects.filter(status=ACTIVE)
    model = Entity
    paginate_by = 35

    filterset_class = ProviderFilter

    def get_queryset(self):
        qs = super().get_queryset()
        year = self.kwargs.get('year', settings.CURRENT_BALANCE_YEAR)
        entities = qs.filter(registration_date__year__lte=year)
        return entities.prefetch_related(
            Prefetch(
                "social_balances",
                queryset=EntitySocialBalance.objects.filter(year=year),
                to_attr="social_balance"
            )
        )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = EntitySocialBalance.objects.all().order_by('year').values_list('year', flat=True).distinct()
        context['current_year'] = int(self.kwargs.get('year', settings.CURRENT_BALANCE_YEAR))
        return context


class SocialBalanceEditView(UpdateView):
    form_class = EntityYearBalanceForm
    template_name = 'balance/year/detail.html'
    queryset = EntitySocialBalance.objects.all()
    model = EntitySocialBalance

    def get_object(self, queryset=None):
        entity_id = self.kwargs['entity_pk']
        year = self.kwargs['year']

        return EntitySocialBalance.objects.get(entity__pk=entity_id, year=year)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = Entity.objects.get(pk=self.object.entity.pk)
        context['badge'] = SocialBalanceBadge.objects.filter(year=self.object.year).first()

        return context

    def get_success_url(self):
        messages.success(self.request, _('Datos de balance actualizados satisfactoriamente.'))
        return reverse('balance:entity_year', kwargs={'entity_pk': self.object.entity.pk, 'year':self.object.year })


class ImportSocialBalanceFormView(AjaxFormResponseMixin, FormView):
    template_name = 'balance/year/import.html'
    form_class = ImportSocialBalanceForm

    def form_valid(self, form):

        year = form.cleaned_data['year']
        csv_file = form.cleaned_data['csv_file']

        form.results = EntitySocialBalance.import_data(csv_file, year)
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, _('Datos de balance actualizados satisfactoriamente.'))
        return reverse('balance:bulk_import')


def generate_badge(request, entity_pk, year):

    balance = EntitySocialBalance.objects.get(entity__pk=entity_pk, year=year)

    if request.method == "POST":
        redirect_url = request.POST.get('redirect_to', '')
        balance.render_badge()
        if redirect_url:
            messages.success(request, _('Sello actualizado correctamente.'))
            return redirect(redirect_url)

    return False