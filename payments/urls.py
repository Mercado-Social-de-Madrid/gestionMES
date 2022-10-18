
from django.conf.urls import url

from . import views

app_name = 'payments'

urlpatterns = [

    url(r'^$', views.PaymentsListView.as_view(), name='payments_list'),
    url(r'^create/$', views.PaymentCreate.as_view(), name='create_payment'),
    url(r'^year/(?P<year>\d+)/$', views.PaymentsListView.as_view(), name='list_by_year'),
    url(r'^(?P<pk>[0-9a-f-]+)$', views.PaymentDetailView.as_view(), name='payment_detail'),
    url(r'^(?P<pk>[0-9a-f-]+)/update/$', views.update_payment, name='update_payment'),
    url(r'^(?P<pk>[0-9a-f-]+)/delete/$', views.payment_delete, name='payment_delete'),
    url(r'^(?P<pk>[0-9a-f-]+)/fee/$', views.assign_payment_to_annualfeecharge, name='assign_fee'),
    url(r'^card/$', views.CardPaymentsListView.as_view(), name='card_payments_list'),
    url(r'^card/(?P<pk>[0-9a-f-]+)/$', views.CardPaymentDetailView.as_view(), name='card_payment_detail'),
    url(r'^pay/(?P<uuid>[0-9a-f-]+)/$', views.form, name='payment_form'),
    url(r'^end/success/$', views.payment_success, name='payment_success'),
    url(r'^end/error/$', views.payment_error, name='payment_error'),

    url(r'^(?P<pk>[0-9a-f-]+)/factura.pdf$', views.invoice_pdf, name='invoice_pdf'),

    url(r'^annual/(?P<year>\d+)/$', views.AnnualFeeChargesList.as_view(), name='annual_feecharges'),
    url(r'^annual/(?P<year>\d+)/fee/(?P<pk>\d+)$', views.SplitFeeCharge.as_view(), name='split_feecharge'),

    url(r'^sepa/$', views.SepaBatchListView.as_view(), name='sepa_list'),
    url(r'^sepa/add/$', views.BatchCreate.as_view(), name='sepa_create'),
    url(r'^sepa/update/(?P<pk>[0-9a-f-]+)/$', views.BatchUpdate.as_view(), name='sepa_update'),
    url(r'^sepa/(?P<pk>[0-9a-f-]+)/$', views.BatchDetail.as_view(), name='sepa_detail'),
    url(r'^sepa/(?P<pk>[0-9a-f-]+)/regenerate/$', views.sepa_regenerate, name='sepa_regenerate'),
    url(r'^sepa/(?P<pk>[0-9a-f-]+)/delete/$', views.sepa_delete, name='sepa_delete'),
    url(r'^sepa/(?P<pk>[0-9a-f-]+)/(?P<batch_pk>[0-9a-f-]+)/invoice$', views.batch_payment_pdf, name='batch_payment_pdf'),

    url(r'^banks/$', views.BankList.as_view(), name='bank_list'),
    url(r'^banks/bic$', views.BicExplanation.as_view(), name='bic_explanation'),
    url(r'^banks/add/$', views.BankCreate.as_view(), name='bank_create'),
    url(r'^banks/(?P<pk>[0-9a-f-]+)/$', views.BankUpdate.as_view(), name='bank_detail'),

    url(r'^fees/add_comment/$', views.add_fee_comment, name='add_fee_comment'),
]

