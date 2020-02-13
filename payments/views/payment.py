# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.conf import settings
from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget
from filters.views import FilterMixin

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from payments.forms.payment import PaymentForm, UpdatePaymentForm
from payments.models import PendingPayment


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

    search = SearchFilter(names=['concept', 'account__contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['amount', 'added', 'timestamp'], field_labels={'amount':'Cantidad', 'added':'Añadido', 'timestamp':'Pagado'})
    account = MemberTypeFilter(label='Tipo de socia')
    completed = django_filters.BooleanFilter(field_name='completed', widget=BooleanWidget(attrs={'class':'threestate'}))
    returned = django_filters.BooleanFilter(field_name='returned',
                                             widget=BooleanWidget(attrs={'class': 'threestate'}))

    class Meta:
        model = PendingPayment
        form = PendingPaymentFilterForm
        fields = {  }


class PaymentsListView(FilterMixin, FilterView, ExportAsCSVMixin, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = PendingPayment.objects.all()
    objects_url_name = 'payment_detail'
    template_name = 'payments/list.html'
    ajax_template_name = 'payments/query.html'
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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pending'] = PendingPayment.objects.filter(completed=False).aggregate(sum=Sum('amount'))['sum']
        context['form'] = UpdatePaymentForm()
        context['narrow'] = True
        context['valign'] = True
        return context


class PaymentDetailView(UpdateView):
    template_name = 'payments/detail.html'
    queryset = PendingPayment.objects.all()
    form_class = PaymentForm
    model = PendingPayment

    def form_invalid(self, form):
        res = super().form_invalid(form)
        print (form.errors)
        return res

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
            print(redirect_url)
            if redirect_url:
                messages.success(request, _('Pago actualizado correctamente.'))
                return redirect(redirect_url)

            return HttpResponse(status=200)

        else:
            print('form invalid!')
            print(form.errors)

    return HttpResponse(status=400)



