
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^invite/(?P<uuid>[0-9a-f-]+)/$', views.NewInvite.as_view(), name='invite'),
    url(r'^currency/guests/$', views.InvitesListView.as_view(), name='guest_user_list'),
    url(r'^currency/guests/(?P<pk>\d+)/$', views.GuestAccountDetailView.as_view(), name='guest_detail'),
]


