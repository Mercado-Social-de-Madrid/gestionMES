
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.PaymentsListView.as_view(), name='payments_list'),
    url(r'^det/(?P<pk>[0-9a-f-]+)$', views.PaymentsListView.as_view(), name='payment_detail'),
    url(r'^pay/$', views.form, name='payment_form'),
    url(r'^end/$', views.end, name='end'),
]


