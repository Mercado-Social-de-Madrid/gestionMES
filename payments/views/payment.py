# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Sum, Count, Max
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget
from filters.views import FilterMixin

from accounts.custom_filters import AccountSearchFilter
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from payments.forms.payment import PaymentForm, UpdatePaymentForm
from payments.models import PendingPayment, SepaPaymentsBatch


class MemberTypeFilter(django_filters.ChoiceFilter):

    def __init__(self, *args,**kwargs):
        django_filters.ChoiceFilter.__init__(self, choices=settings.MEMBER_TYPES, *args,**kwargs)

    def filter(self,qs,value):
        if value not in (None,''):
            qs = qs.filter(account__member_type=value)
        return qs


class PendingPaymentFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class PendingPaymentFilter(django_filters.FilterSet):

    search = AccountSearchFilter(names=['concept', 'account__cif'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(
        choices=(('-added', 'Añadido'), ('-amount', 'Cantidad (descendente)'), ('-timestamp','Pagado'), ('-sepa_batches__attempt','Añadido a remesa')) )
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
    available_fields = ['account', 'reference', 'amount', 'concept', 'type', 'completed', 'timestamp', 'revised_by', 'comment', 'added' ]

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
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        fee = self.object.fee_charges.first()
        if fee:
            fee.payment_updated()

        return response

    def get_success_url(self):
        return reverse('payments:payment_detail', kwargs={'pk': self.object.pk})


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
