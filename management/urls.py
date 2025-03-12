
from django.urls import path

from . import views

app_name = 'management'

urlpatterns = [

    path('users/', views.UsersListView.as_view(), name='users_list'),
    path('users/add/', views.UsersCreate.as_view(), name='user_add'),
    path('users/(?P<pk>\d+)/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/(?P<pk>\d+)/delete/', views.user_delete, name='delete_user'),

    path('comm/', views.ComissionsListView.as_view(), name='commission_list'),
    path('comm/add/', views.CommissionCreate.as_view(), name='commission_add'),
    path('comm/(?P<pk>\d+)/', views.CommissionDetailView.as_view(), name='commission_detail'),
    path('comm/(?P<pk>\d+)/members/', views.CommissionMembers.as_view(), name='commission_members'),

]


