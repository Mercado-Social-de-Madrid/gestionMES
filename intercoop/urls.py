
from django.conf.urls import url

from . import views

app_name='intercoop'

urlpatterns = [

    url(r'^accounts/$', views.IntercoopAccountsList.as_view(), name='accounts_list'),
    url(r'^accounts/(?P<pk>[0-9a-f-]+)/$', views.AccountDetail.as_view(), name='account_detail'),
    url(r'^entity/$', views.EntityList.as_view(), name='entity_list'),
    url(r'^entity/add/$', views.EntityCreate.as_view(), name='add_entity'),
    url(r'^entity/(?P<pk>[0-9a-f-]+)/$', views.EntityDetail.as_view(), name='entity_detail'),

    url(r'^(?P<slug>[0-9a-zA-Z_-]+)/$', views.AccountSlugCreate.as_view(), name='account_create'),

]


