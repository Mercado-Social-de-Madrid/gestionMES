
from django.urls import path

from . import views

app_name='currency'

urlpatterns = [
    path('invite/success/', views.InviteSuccessView.as_view(), name='invite_success'),
    path('invite/', views.NewInvite.as_view(), name='invite'),
    path('invite/<uuid>/', views.NewInvite.as_view(), name='invite'),
    path('currency/guests/', views.InvitesListView.as_view(), name='guest_user_list'),
    path('currency/guests/<int:pk>/', views.GuestAccountDetailView.as_view(), name='guest_detail'),
    path('currency/add_app_user/', views.add_app_user, name='add_app_user'),
    path('currency/fetch_account/', views.fetch_acccount_info, name='fetch_acccount_info'),
]


