
from django.conf.urls import url

from . import views

app_name = 'payments'

urlpatterns = [

    url(r'^$', views.PaymentsListView.as_view(), name='payments_list'),
    url(r'^(?P<pk>[0-9a-f-]+)$', views.PaymentDetailView.as_view(), name='payment_detail'),
    url(r'^card/$', views.CardPaymentsListView.as_view(), name='card_payments_list'),
    url(r'^card/(?P<pk>[0-9a-f-]+)/$', views.CardPaymentDetailView.as_view(), name='card_payment_detail'),
    url(r'^pay/(?P<uuid>[0-9a-f-]+)/$', views.form, name='payment_form'),
    url(r'^end/success/$', views.payment_success, name='payment_success'),
    url(r'^end/error/$', views.payment_error, name='payment_error'),
]

