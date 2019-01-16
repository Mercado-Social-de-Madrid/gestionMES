# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.contrib.sites.models import Site
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView, DetailView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.forms.consumer import ConsumerForm
from accounts.forms.process import SignupProcessForm
from accounts.forms.provider import ProviderForm
from accounts.models import Provider, Consumer, SignupProcess
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.forms.password import PasswordForm
from core.forms.profile import ProfileForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.models import User
from mes import settings
from simple_bpm.custom_filters import WorkflowFilter
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.conf import settings
from sermepa.forms import SermepaPaymentForm
from sermepa.signals import payment_was_successful, payment_was_error, signature_error
from sermepa.models import SermepaIdTPV
from simple_bpm.forms.WorkflowEventForm import WorkflowEventForm


class ProviderFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class ProviderFilter(django_filters.FilterSet):

    search = SearchFilter(names=['address', 'name', 'business_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'start_year', 'registration_date'])

    class Meta:
        model = Provider
        form = ProviderFilterForm
        fields = { 'status':['exact'], }


class PaymentsListView(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = Provider.objects.all()
    objects_url_name = 'provider_detail'
    template_name = 'provider/list.html'
    ajax_template_name = 'provider/query.html'
    filterset_class = ProviderFilter
    paginate_by = 15





def form(request, trans_type='0'):
    site = Site.objects.get_current()
    amount = int(5.50 * 100)  # El precio es en céntimos de euro

    sermepa_dict = {
        "Ds_Merchant_Titular": 'John Doe',
        "Ds_Merchant_MerchantData": 12345,  # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
        "Ds_Merchant_MerchantName": settings.SERMEPA_MERCHANT_NAME,
        "Ds_Merchant_ProductDescription": 'Pago inicial',
        "Ds_Merchant_Amount": amount,
        "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
        "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
        "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
        "Ds_Merchant_MerchantURL": "http://%s%s" % (site.domain, reverse('sermepa_ipn')),
        "Ds_Merchant_UrlOK": "http://%s%s" % (site.domain, reverse('end')),
        "Ds_Merchant_UrlKO": "http://%s%s" % (site.domain, reverse('end')),
    }

    if trans_type == '0':  # Compra puntual
        order = SermepaIdTPV.objects.new_idtpv()  # Tiene que ser un número único cada vez
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == 'L':  # Compra recurrente por fichero. Cobro inicial
        order = SermepaIdTPV.objects.new_idtpv()  # Tiene que ser un número único cada vez
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == 'M':  # Compra recurrente por fichero. Cobros sucesivos
        order = suscripcion.idtpv  # Primer idtpv, 10 dígitos
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '0':  # Compra recurrente por Referencia. Cobro inicial
        order = 'REQUIRED'
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '0':  # Compra recurrente por Referencia. Cobros sucesivos
        order = suscripcion.idreferencia  # Primer idtpv, 10 dígitos
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '3':  # Devolución
        order = suscripcion.idreferencia  # Primer idtpv, 10 dígitos
        sermepa_dict.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
            "Ds_Merchant_AuthorisationCode": pedido.Ds_AuthorisationCode,  # Este valor sale
            # de la SermepaResponse obtenida del cobro que se quiere devolver.
        })

    print sermepa_dict
    form = SermepaPaymentForm(initial=sermepa_dict, merchant_parameters=sermepa_dict)

    return HttpResponse(render_to_response('payments/pay_form.html', {'form': form, 'debug': settings.DEBUG}))


def end(request):
    return HttpResponse(render_to_response('end.html', {}))


def payment_ok(sender, **kwargs):
    pass


def payment_ko(sender, **kwargs):
    pass


def sermepa_ipn_error(sender, **kwargs):
    pass


payment_was_successful.connect(payment_ok)
payment_was_error.connect(payment_ko)
signature_error.connect(sermepa_ipn_error)