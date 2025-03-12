
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name='dashboard'

urlpatterns = [
    path('', views.dashboard.as_view(), name='index'),
    path('accounts/', views.accounts.as_view(), name='accounts'),
    path('signups/', views.signups.as_view(), name='signups'),
    path('intercoop/', views.intercoop.as_view(), name='intercoop'),
]


