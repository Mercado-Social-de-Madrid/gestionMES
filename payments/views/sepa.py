# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from helpers import FilterMixin

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from payments.forms.sepa import SepaBatchForm, UpdateBatchForm
from payments.models import SepaBatchResult
from payments.models import SepaPaymentsBatch


class SepaBatchFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class SepaBatchFilter(django_filters.FilterSet):

    search = SearchFilter(names=['title'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['amount', 'attempt'], field_labels={'amount':'Cantidad', 'attempt':'Fecha', })

    class Meta:
        model = SepaPaymentsBatch
        form = SepaBatchFilterForm
        fields = ['generated_by']


class SepaBatchListView(PermissionRequiredMixin, FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'payments.mespermission_can_manage_sepa'
    queryset = SepaPaymentsBatch.objects.all()
    objects_url_name = 'sepa_detail'
    template_name = 'payments/sepa/list.html'
    ajax_template_name = 'payments/sepa/query.html'
    filterset_class = SepaBatchFilter
    ordering = ['-attempt']
    paginate_by = 15
    model = SepaPaymentsBatch

    def get_queryset(self):
        return super().get_queryset().annotate(payments_count=Count('payments'))


class BatchCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'payments.mespermission_can_manage_sepa'
    form_class = SepaBatchForm
    model = SepaPaymentsBatch
    template_name = 'payments/sepa/create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Fichero SEPA creado correctamente.'))
        return response

    def get_success_url(self):
        return reverse('payments:sepa_detail', kwargs={'pk': self.object.pk})


class BatchUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'payments.mespermission_can_manage_sepa'
    form_class = UpdateBatchForm
    model = SepaPaymentsBatch
    template_name = 'payments/sepa/update.html'

    def get_success_url(self):
        return reverse('payments:sepa_detail', kwargs={'pk': self.kwargs.get("pk")})


class BatchDetail(PermissionRequiredMixin, ExportAsCSVMixin, UpdateView):
    permission_required = 'payments.mespermission_can_manage_sepa'
    form_class = UpdateBatchForm
    filterset_fields = []
    template_name = 'payments/sepa/detail.html'
    queryset = SepaPaymentsBatch.objects.all()
    model = SepaPaymentsBatch

    available_fields = ['account_name', 'payment_amount', 'account_iban', 'iban_code', 'bic_code', 'bank_name', 'success', 'fail_reason_display']
    field_labels = {'account_name': 'Cuenta',
                    'payment_amount': 'Cantidad',
                    'account_iban': 'IBAN',
                    'iban_code': 'Código entidad bancaria',
                    'bic_code': 'Código BIC',
                    'bank_name': 'Nombre entidad',
                    'success':'Añadido',
                    'fail_reason_display':'Motivo fallo'}

    def get_list_to_export(self):
        return SepaBatchResult.objects.filter(batch=self.get_object()).order_by('order' )

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['batch_results'] = self.get_list_to_export()
        context['batch_success'] = SepaBatchResult.objects.filter(batch=self.object, success=True).count()
        return context

    def form_valid(self, form):
        self.object.preprocess_batch()
        self.object.generate_batch()
        messages.success(self.request, _('Remesa SEPA generada correctamente.'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('payments:sepa_detail', kwargs={'pk': self.object.pk})


def sepa_regenerate(request, pk):
    sepa = SepaPaymentsBatch.objects.get(pk=pk)
    sepa.preprocess_batch()
    sepa.generate_batch()
    messages.success(request, _('Remesa SEPA generada correctamente.'))
    return redirect(reverse('payments:sepa_detail', kwargs={'pk': sepa.pk}))


def sepa_delete(request, pk):
    sepa = SepaPaymentsBatch.objects.get(pk=pk)
    sepa.delete()
    messages.success(request, _('Remesa SEPA eliminada correctamente.'))
    return redirect(reverse('payments:sepa_list'))


def batch_payment_pdf(request, pk, batch_pk):
    sepa = SepaPaymentsBatch.objects.get(pk=pk)
    batch_pay =  SepaBatchResult.objects.get(pk=batch_pk)

    payment = batch_pay.payment
    payment.invoice_prefix = sepa.invoice_prefix
    payment.invoice_number = batch_pay.invoice_number
    payment.invoice_date = sepa.attempt
    payment.save()

    return redirect(reverse('payments:invoice_pdf', kwargs={'pk': payment.pk}))
