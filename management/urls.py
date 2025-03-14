
from django.urls import path

from . import views

app_name = 'management'

urlpatterns = [

    path('users/', views.UsersListView.as_view(), name='users_list'),
    path('users/add/', views.UsersCreate.as_view(), name='user_add'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/delete/', views.user_delete, name='delete_user'),

    path('comm/', views.ComissionsListView.as_view(), name='commission_list'),
    path('comm/add/', views.CommissionCreate.as_view(), name='commission_add'),
    path('comm/<int:pk>/', views.CommissionDetailView.as_view(), name='commission_detail'),
    path('comm/<int:pk>/members/', views.CommissionMembers.as_view(), name='commission_members'),

]


