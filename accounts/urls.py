
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [

    path('', views.AccountListView.as_view(), name='list'),

    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreate.as_view(), name='add_category'),
    path('categories/<pk>/', views.CategoryDetailView.as_view(), name='category_detail'),

    path('collab/', views.CollaborationListView.as_view(), name='collab_list'),
    path('collab/add', views.CollaborationCreate.as_view(), name='collab_new'),
    path('collab/<int:pk>/', views.CollaborationDetailView.as_view(), name='collab_detail'),

    path('entities/', views.EntitiesListView.as_view(), name='entity_list'),
    path('entities/add', views.CreateEntity.as_view(), name='add_entity'),
    path('entities/<int:pk>/', views.EntityDetailView.as_view(), name='entity_detail'),
    path('entities/collab/add/', views.EntityCollaborationCreate.as_view(), name='collab_entity_add'),
    path('entities/collab/<int:pk>/', views.EntityCollaborationUpdate.as_view(), name='collab_entity_update'),

    path('providers/', views.ProvidersListView.as_view(), name='providers_list'),
    path('providers/<int:pk>/', views.ProviderDetailView.as_view(), name='provider_detail'),
    path('providers/<int:pk>/delete', views.delete_account, name='provider_delete'),

    path('consumers/', views.ConsumersListView.as_view(), name='consumers_list'),
    path('consumers/<int:pk>/', views.ConsumerDetailView.as_view(), name='consumer_detail'),
    path('consumers/<int:pk>/delete', views.delete_account, name='consumer_delete'),

    path('signup/add/', views.NewSignup.as_view(), name='add_signup'),
    path('signup/consumer/', views.ConsumerSignup.as_view(), name='consumer_signup_form'),
    path('signup/provider/', views.ProviderSignup.as_view(), name='provider_signup_form'),
    path('signup/provider/<uuid>/', views.ProviderUpdateView.as_view(), name='provider_edit_form'),
    path('signup/consumer/<uuid>/', views.ConsumerUpdateView.as_view(), name='consumer_edit_form'),

    path('signup/success/', views.SignupSuccessView.as_view(), name='signup_success'),
    path('signup/processes/', views.SignupListView.as_view(), name='signup_list'),
    path('signup/processes/<int:pk>/', views.SignupDetailView.as_view(), name='signup_detail'),
    path('signup/processes/cancel/', views.cancel_signup, name='cancel_signup'),
    path('signup/<uuid>/', views.signup_form_redirect, name='signup_form'),

    path('deletion/processes/', views.DeletionListView.as_view(), name='deletion_list'),
    path('deletion/processes/<int:pk>/', views.DeletionDetailView.as_view(), name='deletion_detail'),
    path('deletion/processes/cancel/', views.cancel_delete, name='cancel_deletion'),
    path('deletion/processes/revert/', views.revert_delete, name='revert_deletion'),

    path('catalogo/', views.CatalogListView.as_view(), name='catalog_list'),

    path('reports/', views.AccountsReportView.as_view(), name='accounts_report'),

    path('capitales_sociales/', views.SocialCapitalListView.as_view(), name='social_capital_list'),
    path('capitales_sociales/<int:pk>/', views.SocialCapitalDetailView.as_view(), name='social_capital_detail'),
]


