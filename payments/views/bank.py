# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.db.models import Count
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from payments.forms.bank import BankForm
from payments.forms.sepa import SepaBatchForm
from payments.models import SepaBatchResult, BankBICCode
from payments.models import SepaPaymentsBatch


class BankFilterForm(BootstrapForm):
    field_order = ['search', ]


class BankFilter(django_filters.FilterSet):
    search = SearchFilter(names=['bank_name', 'bic_code'], lookup_expr='in', label=_('Buscar...'))

    class Meta:
        model = SepaPaymentsBatch
        form = BankFilterForm
        fields = []


class BankList(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = BankBICCode.objects.all()
    objects_url_name = 'bank_detail'
    template_name = 'payments/bank/list.html'
    ajax_template_name = 'payments/bank/query.html'
    filterset_class = BankFilter
    ordering = ['bank_code']
    paginate_by = 15
    model = BankBICCode


class BankCreate(CreateView):

    form_class = BankForm
    model = BankBICCode
    template_name = 'payments/bank/create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Entidad bancaria añadida correctamente.'))
        return response

    def get_success_url(self):
        return reverse('payments:bank_detail', kwargs={'pk': self.object.pk})


class BankUpdate(UpdateView):
    template_name = 'payments/bank/detail.html'
    form_class = BankForm
    model = BankBICCode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('payments:bank_list')

