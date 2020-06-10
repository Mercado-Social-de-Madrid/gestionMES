# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import gettext as _
from django.views.generic import UpdateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.ModelFieldsViewMixin import ModelFieldsViewMixin
from payments.forms.payment import PaymentForm
from payments.models import CardPayment


class CardPaymentFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class CardPaymentFilter(django_filters.FilterSet):

    search = SearchFilter(names=['reference', 'account__contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['amount', 'attempt'], field_labels={'amount':'Cantidad', 'attempt':'Fecha'})

    class Meta:
        model = CardPayment
        form = CardPaymentFilterForm
        fields = { 'type':['exact'] }

class CardPaymentsListView(PermissionRequiredMixin, FilterMixin, FilterView, ExportAsCSVMixin, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'payments.mespermission_can_view_card_payments'
    queryset = CardPayment.objects.filter(paid=True).order_by('-attempt')
    filterset_class = CardPaymentFilter
    objects_url_name = 'card_payment_detail'
    template_name = 'card/list.html'
    ajax_template_name = 'card/query.html'
    paginate_by = 12

    model = CardPayment

    csv_filename = 'card'
    available_fields = ['account', 'attempt', 'amount', 'reference', 'concept', 'type', 'paid', 'pending_payment', ]
    field_labels = {'concept': 'Concepto', }


class CardPaymentDetailView(PermissionRequiredMixin, ModelFieldsViewMixin, UpdateView):
    permission_required = 'payments.mespermission_can_view_card_payments'
    template_name = 'card/detail.html'
    queryset = CardPayment.objects.all()
    form_class = PaymentForm
    model = CardPayment
