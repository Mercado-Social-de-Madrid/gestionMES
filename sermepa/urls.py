from django.conf.urls import url

from . import views


urlpatterns = [
    url(regex=r'^$', view=views.sermepa_ipn, name='sermepa_ipn'),
    url(r'^(?P<pk>[0-9a-f-]+)$', views.SermepaResponseDetailView.as_view(), name='sermepa_response')
]
