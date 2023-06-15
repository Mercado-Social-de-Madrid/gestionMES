# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import django_filters
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, FormView
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget

from accounts.custom_filters import AccountSearchFilter
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers import FilterMixin
from simple_bpm.custom_filters import WorkflowFilter
from simple_bpm.forms.WorkflowEventForm import WorkflowEventForm
from simple_bpm.views import cancel_process
from social_balance.forms.generate_process import GenerateProcessForm
from social_balance.forms.process import ProcessSponsorForm
from social_balance.models import BalanceProcess, BALANCE_TYPES


class SponsorFilter(django_filters.BooleanFilter):
    def filter(self, qs, value):
        return qs.filter(sponsor=self.parent.request.user) if value == True else qs


class BalanceProcessYearFilter(django_filters.ChoiceFilter):

    def __init__(self, *args,**kwargs):
        years_map = list(BalanceProcess.objects.values('year').distinct().order_by('year'))
        years = list(map(lambda x: str(x['year']), years_map))
        years_labeled = list(zip(years, years))
        django_filters.ChoiceFilter.__init__(self, choices=years_labeled, *args,**kwargs)

    def filter(self, qs, value):
        if value:
            qs = qs.filter(year=value)
        return qs


class BalanceFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'balance_type', 'status', 'year']


class BalanceFilter(django_filters.FilterSet):

    search = AccountSearchFilter(names=['sponsor__username', 'account__cif'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['account', 'last_update'], field_labels={'account':'Nombre', 'last_update':'Última actualización'})
    status = WorkflowFilter(['social_balance'], filter_cancelled=True, filter_completed=True, label='Estado')
    balance_type = django_filters.ChoiceFilter(choices=BALANCE_TYPES, label=_('Tipo:'))
    year = BalanceProcessYearFilter(label='Año')
    sponsor = SponsorFilter(label=_('Amadrinada por mí'), widget=BooleanWidget(attrs={'class':'threestate'}))

    class Meta:
        form = BalanceFilterForm
        fields = { }


class BalanceProcessList(PermissionRequiredMixin, FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'social_balance.mespermission_can_view_balance_process'
    queryset = BalanceProcess.objects.all().order_by('-year')
    objects_url_name = 'process_detail'
    template_name = 'balance/process/list.html'
    ajax_template_name = 'balance/process/query.html'
    filterset_class = BalanceFilter
    paginate_by = 15

    def get_queryset(self):

        year = self.kwargs.get('year_create', None)
        if year:
            year = int(year)
            BalanceProcess.objects.create_pending_processes(year)
            return BalanceProcess.objects.filter(year=year).order_by('-last_update')

        return super().get_queryset()


class BalanceProcessGenerate(PermissionRequiredMixin, FormView):
    permission_required = 'social_balance.mespermission_can_view_balance_process'
    template_name = 'balance/process/generate.html'
    form_class = GenerateProcessForm
    success_url = reverse_lazy('balance:process_list')

    def get_initial(self):
        return { 'year': datetime.now().year - 1 }

    def form_valid(self, form):
        year = form.cleaned_data['year']
        balance_type = form.cleaned_data['balance_type']

        BalanceProcess.objects.create_pending_processes(year, balance_type)
        messages.success(self.request, _('Procesos anuales generados correctamente.'))
        return super().form_valid(form)

class BalanceProcessDetail(PermissionRequiredMixin, UpdateView):
    permission_required = 'social_balance.mespermission_can_view_balance_process'
    template_name = 'balance/process/detail.html'
    queryset = BalanceProcess.objects.all()
    form_class = ProcessSponsorForm
    model = BalanceProcess

    def get_success_url(self):
        return reverse('balance:process_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.sponsor_updated(self.request.user)
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['previous_balance'] = BalanceProcess.objects.filter(account=self.object.account, year=(self.object.year-1)).first()

        if self.object.workflow.is_first_step():
            context['first_step'] = True

        form = WorkflowEventForm(initial={
            'workflow':context['object'].workflow,
            'redirect_to': reverse('balance:process_detail', kwargs={'pk': self.object.pk})
        })
        context['step_form'] = form
        return context


def cancel(request):
    return cancel_process(request, BalanceProcess)