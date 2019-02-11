
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^invite/(?P<uuid>[0-9a-f-]+)/$', views.NewInvite.as_view(), name='invite'),
]


