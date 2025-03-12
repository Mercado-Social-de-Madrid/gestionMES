
from django.urls import path

from . import views

app_name='intercoop'

urlpatterns = [

    path('accounts/', views.IntercoopAccountsList.as_view(), name='accounts_list'),
    path('accounts/<pk>/', views.AccountDetail.as_view(), name='account_detail'),
    path('accounts/<pk>/validate/', views.validate_account, name='validate_account'),
    path('accounts/<pk>/delete/', views.account_delete, name='account_delete'),

    path('entity/', views.EntityList.as_view(), name='entity_list'),
    path('entity/add/', views.EntityCreate.as_view(), name='add_entity'),
    path('entity/<pk>/', views.EntityDetail.as_view(), name='entity_detail'),

    path('<slug>/', views.AccountSlugCreate.as_view(), name='account_create'),

]


