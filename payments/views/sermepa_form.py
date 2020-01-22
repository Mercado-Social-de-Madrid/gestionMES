# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_exempt
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
from payments.forms.FeeComment import FeeCommentForm
from payments.forms.payment import PaymentForm, UpdatePaymentForm
from payments.models import PendingPayment, CardPayment
from sermepa.forms import SermepaPaymentForm
from sermepa.models import SermepaIdTPV
from sermepa.signals import payment_was_successful, payment_was_error, signature_error


def generate_payment_form(payment_uuid, URL_params=''):
    site = Site.objects.get_current()
    merchant_data = 0
    trans_type = '0'
    card_payment, already_paid = PendingPayment.objects.get_card_payment(reference=payment_uuid)

    if already_paid:
        return True, None, None

    if card_payment:
        merchant_data = card_payment.pk
        amount = int(card_payment.amount * 100)
    else:
        return False, None, None

    # Redirect to local processor if we are in debug
    view_OK = 'sermepa_ipn' if settings.SERMEPA_DEBUG else 'payments:payment_success'
    view_KO = 'sermepa_ipn' if settings.SERMEPA_DEBUG else 'payments:payment_error'

    sermepa_dict = {
        "Ds_Merchant_Titular": card_payment.account.display_name,
        "Ds_Merchant_MerchantData": merchant_data,
        "Ds_Merchant_MerchantName": settings.SERMEPA_MERCHANT_NAME,
        "Ds_Merchant_ProductDescription": card_payment.concept,
        "Ds_Merchant_Amount": amount,
        "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
        "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
        "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
        "Ds_Merchant_MerchantURL": "https://%s%s" % (site.domain, reverse('sermepa_ipn')),
        "Ds_Merchant_UrlOK": "https://%s%s" % (site.domain, reverse(view_OK)) + URL_params,
        "Ds_Merchant_UrlKO": "https://%s%s" % (site.domain, reverse(view_KO)) + URL_params,
    }

    order = SermepaIdTPV.objects.new_idtpv()
    sermepa_dict.update({
        "Ds_Merchant_Order": order,
        "Ds_Merchant_TransactionType": trans_type,
    })
    form = SermepaPaymentForm(initial=sermepa_dict, merchant_parameters=sermepa_dict)

    return False, card_payment, form



@xframe_options_exempt
def form(request, uuid):

    # print "http://%s%s" % (site.domain, reverse('sermepa_ipn'))
    params = '' if not 'from_app' in request.GET else '?from_app=true'

    payment = PendingPayment.objects.filter(reference=uuid).first()
    if payment and payment.completed:
        return HttpResponse(render_to_response('payments/pay_form_paid.html',
                                               {'request': request, 'uuid': uuid, 'payment': payment}))

    paid, card_payment, form = generate_payment_form(uuid, URL_params=params)
    if paid:
        return HttpResponse(render_to_response('payments/pay_form_paid.html',
                                               {'request': request, 'uuid': uuid, 'payment': payment,
                                                'card_payment': card_payment}))

    return HttpResponse(render_to_response('payments/pay_form.html',
                                           {'request': request, 'uuid': uuid, 'payment': payment, 'form': form,
                                            'card_payment': card_payment, 'debug': settings.SERMEPA_DEBUG}))


@xframe_options_exempt
def payment_success(request):
    return HttpResponse(render_to_response('payments/end.html', {}))

@xframe_options_exempt
def payment_error(request):
    return HttpResponse(render_to_response('payments/error.html', {}))


def payment_ok(sender, **kwargs):
    print('Payment ok!')
    PendingPayment.objects.process_sermepa_payment(sender)


def payment_ko(sender, **kwargs):
    print('Payment bad!')


def sermepa_ipn_error(sender, **kwargs):
    print('ipn error!')


payment_was_successful.connect(payment_ok)
payment_was_error.connect(payment_ko)
signature_error.connect(sermepa_ipn_error)