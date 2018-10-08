
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^users/$', views.UsersListView.as_view(), name='users_list'),
    url(r'^users/add/$', views.UsersCreate.as_view(), name='user_add'),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetailView.as_view(), name='user_detail'),

    url(r'^comm/$', views.ComissionsListView.as_view(), name='commission_list'),
    url(r'^comm/add/$', views.CommissionCreate.as_view(), name='commission_add'),
    url(r'^comm/(?P<pk>\d+)/$', views.CommissionDetailView.as_view(), name='commission_detail'),
    url(r'^comm/(?P<pk>\d+)/members/$', views.CommissionMembers.as_view(), name='commission_members'),

]


