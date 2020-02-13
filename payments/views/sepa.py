# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.db.models import Sum, Count
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget
from filters.views import FilterMixin

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from payments.forms.payment import UpdatePaymentForm
from payments.models import PendingPayment
from payments.models.sepa import SepaBatch


class SepaBatchFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class SepaBatchFilter(django_filters.FilterSet):

    search = SearchFilter(names=['concept', 'account__contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['amount', 'attempt'], field_labels={'amount':'Cantidad', 'attempt':'Fecha', })
    completed = django_filters.BooleanFilter(field_name='completed', widget=BooleanWidget(attrs={'class':'threestate'}))
    returned = django_filters.BooleanFilter(field_name='returned',
                                             widget=BooleanWidget(attrs={'class': 'threestate'}))
    class Meta:
        model = SepaBatch
        form = SepaBatchFilterForm
        fields = {  }


class SepaBatchListView(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = SepaBatch.objects.all()
    objects_url_name = 'payment_detail'
    template_name = 'payments/sepa/list.html'
    ajax_template_name = 'payments/sepa/query.html'
    filterset_class = SepaBatchFilter
    ordering = ['-attempt']
    paginate_by = 15
    model = SepaBatch

    def get_queryset(self):
        return super().get_queryset().annotate(payments_count=Count('payments'))
