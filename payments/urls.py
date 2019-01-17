
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.PaymentsListView.as_view(), name='payments_list'),
    url(r'^det/(?P<pk>[0-9a-f-]+)$', views.PaymentDetailView.as_view(), name='payment_detail'),
    url(r'^card/', views.CardPaymentsListView.as_view(), name='card_payments_list'),
    url(r'^pay/$', views.form, name='payment_form'),
    url(r'^end/$', views.end, name='end'),
]

