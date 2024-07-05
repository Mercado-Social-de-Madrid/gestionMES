# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView
from django_filters import Filter
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget

from accounts.custom_filters import AccountSearchFilter
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.MemberTypeFilter import MemberTypeFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers import FilterMixin
from helpers.pdf import render_pdf_response
from payments.forms.payment import PaymentForm, UpdatePaymentForm
from payments.models import PendingPayment, SepaPaymentsBatch, AnnualFeeCharges, AccountAnnualFeeCharge


class PendingPaymentFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class PendingPaymentFilter(django_filters.FilterSet):

    search = AccountSearchFilter(names=['concept', 'account__cif'], lookup_expr='in', label=_('Buscar...'))
    invoice_number = Filter(field_name='invoice_number', lookup_expr='exact', label=_('Número de factura...'))
    o = LabeledOrderingFilter(
        choices=(('-added', 'Fecha de emisión'), ('-amount', 'Cantidad (descendente)'), ('-timestamp','Fecha de pago'), ('-sepa_batches__attempt','Añadido a remesa')) )
    account = MemberTypeFilter(label='Tipo de socia')
    completed = django_filters.BooleanFilter(field_name='completed', widget=BooleanWidget(attrs={'class':'threestate'}))
    returned = django_filters.BooleanFilter(field_name='returned', widget=BooleanWidget(attrs={'class': 'threestate'}))

    class Meta:
        model = PendingPayment
        form = PendingPaymentFilterForm
        fields = {  }


class PaymentsListView(PermissionRequiredMixin, FilterMixin, FilterView, ExportAsCSVMixin, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'payments.mespermission_can_view_payments'
    queryset = PendingPayment.objects.all()
    objects_url_name = 'payment_detail'
    template_name = 'payments/list.html'
    ajax_template_name = 'payments/query.html'
    external_template_name = 'payments/query_wrapper.html'
    filterset_class = PendingPaymentFilter
    ordering = ['-added']
    paginate_by = 15
    simple_paginate_by = 8

    model = PendingPayment
    csv_filename = 'pagos'
    available_fields = ['account', 'reference', 'invoice_code', 'amount', 'concept', 'type', 'completed', 'timestamp', 'revised_by',
                        'contact_email', 'contact_phone', 'comment', 'added', 'returned', 'returned_timestamp', 'returned_reason' ]
    field_labels = {'contact_email': 'Email de contacto', 'contact_phone': 'Telefono de contacto',
                    'invoice_code': 'Número de factura'}


    def get_paginate_by(self, queryset):
        if 'simple' in self.request.GET:
            return self.simple_paginate_by
        else:
            return self.paginate_by

    def get_template_names(self):
        if self.request.is_ajax() and 'simple' in self.request.GET:
            return [self.external_template_name]
        else:
            return super().get_template_names()

    def get_queryset(self):
        qs = super().get_queryset()
        year = self.get_current_year()
        if year is not None:
            qs = qs.filter(added__year=year)
        return qs

    def get_current_year(self):
        by_param = self.kwargs.get('year', None)
        return int(by_param) if by_param else None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pending'] = PendingPayment.objects.filter(completed=False).aggregate(sum=Sum('amount'))['sum']
        context['years'] = PendingPayment.objects.dates('added','year').distinct()
        context['current_year'] = self.get_current_year()
        context['form'] = UpdatePaymentForm()
        context['narrow'] = True
        context['valign'] = True
        return context


class PaymentCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'payments.mespermission_can_edit_payments'
    template_name = 'payments/create.html'
    form_class = PaymentForm
    model = PendingPayment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('payments:payment_detail', kwargs={'pk': self.object.pk})


class PaymentDetailView(UpdateView):
    template_name = 'payments/detail.html'
    queryset = PendingPayment.objects.all()
    form_class = PaymentForm
    model = PendingPayment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sepa_batches'] = SepaPaymentsBatch.objects\
            .annotate(payments_count=Count('batch_payments'))\
            .filter(batch_payments__payment=self.object)

        fee = self.object.related_fee
        if fee:
            context['annual_fee'] = fee.annual_charge.year
            context['split_fee'] = fee.split
        else:
            context['annual_fees'] = AnnualFeeCharges.objects.values_list('year', flat=True)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        fee = self.object.fee_charges.first()
        if fee:
            fee.payment_updated()
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        return response

    def get_success_url(self):
        return reverse('payments:payment_detail', kwargs={'pk': self.object.pk})


def assign_payment_to_annualfeecharge(request, pk):
    if request.method == "POST":
        payment = PendingPayment.objects.get(pk=pk)

        action = request.POST.get('action', None)
        if action == 'add':
            year = request.POST.get('annual_fee', None)
            if year:
                annualCharge = AnnualFeeCharges.objects.get(year=year)
                charge, created = AccountAnnualFeeCharge.objects.get_or_create(account=payment.account, annual_charge=annualCharge, collab=None)
                charge.payment = payment
                charge.manually_modified = True
                charge.save()
                messages.success(request, _('Pago asignado correctamente.'))
                return redirect(reverse('payments:payment_detail', kwargs={'pk': pk}))

        if action == 'remove':
            fee = payment.fee_charges.all().first()
            if fee:
                fee.delete()
                messages.success(request, _('Relación eliminada correctamente.'))
                return redirect(reverse('payments:payment_detail', kwargs={'pk': pk}))

    return HttpResponse(status=400)


def update_payment(request, pk):
    if request.method == "POST":
        payment = PendingPayment.objects.get(pk=pk)
        form = UpdatePaymentForm(request.POST,)
        if form.is_valid():
            payment.completed = True
            payment.timestamp = form.cleaned_data.get('timestamp')
            payment.revised_by = request.user
            payment.save()

            redirect_url = form.cleaned_data.get('redirect_to')
            if redirect_url:
                messages.success(request, _('Pago actualizado correctamente.'))
                return redirect(redirect_url)

            return HttpResponse(status=200)

        else:
            print('form invalid!')
            print(form.errors)

    return HttpResponse(status=400)


def payment_delete(request, pk):
    if request.method == "POST":
        payment = PendingPayment.objects.get(pk=pk)
        payment.delete()
        messages.success(request, _('Pago eliminado correctamente.'))
        return redirect(reverse('payments:payments_list'))
    else:
        return HttpResponse(status=400)


def invoice_pdf(request, pk):
    payment = PendingPayment.objects.get(pk=pk)

    invoice_code = payment.invoice_code
    filename = 'factura_{}'.format(invoice_code)
    return render_pdf_response(request, 'pdf/invoice.html',
               {'payment': payment,
                'invoice_code': invoice_code,
                'iban': settings.SEPA_CONFIG['IBAN']}, filename=filename)
