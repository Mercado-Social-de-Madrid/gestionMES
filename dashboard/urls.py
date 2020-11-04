
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name='dashboard'

urlpatterns = [
    url(r'^$', views.dashboard.as_view(), name='index'),
    url(r'^accounts/$', views.accounts.as_view(), name='accounts'),
    url(r'^signups/$', views.signups.as_view(), name='signups'),
    url(r'^intercoop/$', views.intercoop.as_view(), name='intercoop'),
]


