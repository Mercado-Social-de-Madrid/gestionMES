
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^invite/success/$', views.InviteSuccessView.as_view(), name='invite_success'),
    url(r'^invite/(?P<uuid>[0-9a-zA-Z\-]+)/$', views.NewInvite.as_view(), name='invite'),
    url(r'^currency/guests/$', views.InvitesListView.as_view(), name='guest_user_list'),
    url(r'^currency/guests/(?P<pk>\d+)/$', views.GuestAccountDetailView.as_view(), name='guest_detail'),
    url(r'^currency/add_app_user/$', views.add_app_user, name='add_app_user'),

]


