# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import json

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from .models import SermepaResponse
from .mixins import SermepaMixin


class SermepaPaymentForm(SermepaMixin, forms.Form):
    Ds_SignatureVersion = forms.IntegerField(widget=forms.HiddenInput())
    Ds_MerchantParameters = forms.IntegerField(widget=forms.HiddenInput())
    Ds_Signature = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        merchant_parameters = kwargs.pop('merchant_parameters', None)
        secret_key = kwargs.pop('secret_key', settings.SERMEPA_SECRET_KEY)  # implementation for django_payments
        super(SermepaPaymentForm, self).__init__(*args, **kwargs)

        if merchant_parameters:
            json_data = json.dumps(merchant_parameters, ensure_ascii=False).encode('utf8')
            order = merchant_parameters['Ds_Merchant_Order']
            b64_params = self.encode_base64(json_data)
            signature = self.get_firma_peticion(order, b64_params, secret_key)
            self.initial['Ds_SignatureVersion'] = settings.SERMEPA_SIGNATURE_VERSION
            self.initial['Ds_MerchantParameters'] = b64_params.decode('utf-8')
            self.initial['Ds_Signature'] = signature.decode('utf-8')

    def render(self):
        return mark_safe(u"""<form id="tpv_form" action="%s" method="post">
            %s
            <input type="submit" name="submit" class="btn btn-primary" alt="Pagar con tarjeta" value="Pagar con tarjeta"/>
        </form>""" % (settings.SERMEPA_URL_PRO, self.as_p()))

    def sandbox(self):
        return mark_safe(u"""<form id="tpv_form" action="%s" method="post">
            %s
            <input type="submit" name="submit" class="btn btn-primary" alt="Pagar con tarjeta" value="Pagar con tarjeta"/>
        </form>""" % (settings.SERMEPA_URL_TEST, self.as_p()))


class SermepaResponseForm(forms.Form):
    Ds_SignatureVersion = forms.CharField(max_length=256)
    Ds_Signature = forms.CharField(max_length=256)
    Ds_MerchantParameters = forms.CharField(max_length=2048)

    Ds_Date = forms.DateField(required=False, input_formats=('%d/%m/%Y',))
    Ds_Hour = forms.TimeField(required=False, input_formats=('%H:%M',))
