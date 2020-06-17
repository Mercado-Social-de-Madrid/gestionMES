# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget
from filters.views import FilterMixin

from accounts.custom_filters import AccountSearchFilter
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from simple_bpm.custom_filters import WorkflowFilter
from simple_bpm.forms.WorkflowEventForm import WorkflowEventForm
from simple_bpm.views import cancel_process
from social_balance.forms.process import ProcessSponsorForm
from social_balance.models import BalanceProcess


class SponsorFilter(django_filters.BooleanFilter):
    def filter(self, qs, value):
        return qs.filter(sponsor=self.parent.request.user) if value == True else qs

class BalanceFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class BalanceFilter(django_filters.FilterSet):

    search = AccountSearchFilter(names=['sponsor__username', 'account__cif'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['account', 'last_update'], field_labels={'account':'Nombre', 'last_update':'Última actualización'})
    status = WorkflowFilter(['social_balance'], filter_cancelled=True, label='Estado')
    sponsor = SponsorFilter(label=_('Amadrinada por mí'), widget=BooleanWidget(attrs={'class':'threestate'}))

    class Meta:
        model = BalanceProcess
        form = BalanceFilterForm
        fields = { }



class BalanceProcessList(PermissionRequiredMixin, FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'social_balance.mespermission_can_view_balance_process'
    queryset = BalanceProcess.objects.pending().order_by('-last_update')
    objects_url_name = 'process_detail'
    template_name = 'balance/process/list.html'
    ajax_template_name = 'balance/process/query.html'
    filterset_class = BalanceFilter
    paginate_by = 15

    def get_queryset(self):

        year = self.kwargs.get('year', None)
        if year:
            year = int(year)
            BalanceProcess.objects.create_pending_processes(year)
            return BalanceProcess.objects.filter(year=year)
        return BalanceProcess.objects.all()

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

        if self.object.workflow.is_first_step():
            context['first_step'] = True

        form = WorkflowEventForm(initial={
            'workflow':context['object'].workflow,
            'redirect_to': reverse('balance:process_detail', kwargs={'pk': self.object.pk})
        })
        context['comment_form'] = form
        return context


def cancel(request):
    return cancel_process(request, BalanceProcess)