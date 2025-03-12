
from django.urls import path

from . import views

app_name='balance'

urlpatterns = [
    path('balance/badges/', views.BadgesListView.as_view(), name='badge_list'),
    path('balance/badges/create', views.NewSocialBadge.as_view(), name='create_badge'),
    path('balance/badges/<int:pk>/', views.SocialBadgeDetailView.as_view(), name='badge_detail'),
    path('balance/badges/<int:pk>/edit/', views.SocialBadgeEditView.as_view(), name='badge_edit'),
    path('balance/render/<int:pk>/', views.SocialBadgeRender.as_view(), name='badge_render'),

    path('balance/', views.SocialBalanceYear.as_view(), name='balance'),
    path('balance/<int:year>/', views.SocialBalanceYear.as_view(), name='balance_year'),
    path('accounts/providers/<int:entity_pk>/balance/<int:year>/', views.SocialBalanceEditView.as_view(), name='entity_year'),
    path('accounts/providers/<int:entity_pk>/balance/<int:year>/renderbadge/', views.generate_badge, name='generate_badge'),

    path('balance/import/', views.ImportSocialBalanceFormView.as_view(), name='bulk_import'),

    path('balance/processes/', views.BalanceProcessList.as_view(), name='process_list'),
    path('balance/processes/generate/', views.BalanceProcessGenerate.as_view(), name='process_generate'),
    path('balance/processes/year/<int:year_create>/', views.BalanceProcessList.as_view(), name='process_list_year'),
    path('balance/processes/<int:pk>/', views.BalanceProcessDetail.as_view(), name='process_detail'),
    path('balance/processes/cancel/', views.cancel, name='cancel_process'),
]


