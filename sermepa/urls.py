from django.conf.urls import url

from .views import sermepa_ipn, SermepaResponseDetailView

urlpatterns = [
    url(regex=r'^$', view=sermepa_ipn, name='sermepa_ipn'),
    url(r'^(?P<pk>[0-9a-f-]+)$', SermepaResponseDetailView.as_view(), name='sermepa_response')
]
