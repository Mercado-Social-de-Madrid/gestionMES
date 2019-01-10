from django.conf.urls import url

from .views import sermepa_ipn


urlpatterns = [
    url(regex=r'^$', view=sermepa_ipn, name='sermepa_ipn'),
]
