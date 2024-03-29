
from django.conf.urls import url

from . import views

app_name = 'accounts'

urlpatterns = [

    url(r'^$', views.AccountListView.as_view(), name='list'),

    url(r'^categories/$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^categories/add/$', views.CategoryCreate.as_view(), name='add_category'),
    url(r'^categories/(?P<pk>[0-9a-f-]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),

    url(r'^collab/$', views.CollaborationListView.as_view(), name='collab_list'),
    url(r'^collab/add$', views.CollaborationCreate.as_view(), name='collab_new'),
    url(r'^collab/(?P<pk>\d+)/$', views.CollaborationDetailView.as_view(), name='collab_detail'),

    url(r'^entities/$', views.EntitiesListView.as_view(), name='entity_list'),
    url(r'^entities/add$', views.CreateEntity.as_view(), name='add_entity'),
    url(r'^entities/(?P<pk>\d+)/$', views.EntityDetailView.as_view(), name='entity_detail'),
    url(r'^entities/collab/add/$', views.EntityCollaborationCreate.as_view(), name='collab_entity_add'),
    url(r'^entities/collab/(?P<pk>\d+)/$', views.EntityCollaborationUpdate.as_view(), name='collab_entity_update'),

    url(r'^providers/$', views.ProvidersListView.as_view(), name='providers_list'),
    url(r'^providers/(?P<pk>\d+)/$', views.ProviderDetailView.as_view(), name='provider_detail'),
    url(r'^providers/(?P<pk>\d+)/delete$', views.delete_account, name='provider_delete'),

    url(r'^consumers/$', views.ConsumersListView.as_view(), name='consumers_list'),
    url(r'^consumers/(?P<pk>\d+)/$', views.ConsumerDetailView.as_view(), name='consumer_detail'),
    url(r'^consumers/(?P<pk>\d+)/delete$', views.delete_account, name='consumer_delete'),

    url(r'^signup/add/$', views.NewSignup.as_view(), name='add_signup'),
    url(r'^signup/consumer/$', views.ConsumerSignup.as_view(), name='consumer_signup_form'),
    url(r'^signup/provider/$', views.ProviderSignup.as_view(), name='provider_signup_form'),
    url(r'^signup/(?P<uuid>[0-9a-f-]+)/$', views.signup_form_redirect, name='signup_form'),
    url(r'^signup/provider/(?P<uuid>[0-9a-f-]+)/$', views.ProviderUpdateView.as_view(), name='provider_edit_form'),
    url(r'^signup/consumer/(?P<uuid>[0-9a-f-]+)/$', views.ConsumerUpdateView.as_view(), name='consumer_edit_form'),

    url(r'^signup/success/$', views.SignupSuccessView.as_view(), name='signup_success'),
    url(r'^signup/processes/$', views.SignupListView.as_view(), name='signup_list'),
    url(r'^signup/processes/(?P<pk>\d+)/$', views.SignupDetailView.as_view(), name='signup_detail'),
    url(r'^signup/processes/cancel/$', views.cancel_signup, name='cancel_signup'),

    url(r'^deletion/processes/$', views.DeletionListView.as_view(), name='deletion_list'),
    url(r'^deletion/processes/(?P<pk>\d+)/$', views.DeletionDetailView.as_view(), name='deletion_detail'),
    url(r'^deletion/processes/cancel/$', views.cancel_delete, name='cancel_deletion'),
    url(r'^deletion/processes/revert/$', views.revert_delete, name='revert_deletion'),

    url(r'^catalogo/$', views.CatalogListView.as_view(), name='catalog_list'),

    url(r'^reports/$', views.AccountsReportView.as_view(), name='accounts_report'),

    url(r'^capitales_sociales/$', views.SocialCapitalListView.as_view(), name='social_capital_list'),
    url(r'^capitales_sociales/(?P<pk>\d+)/$', views.SocialCapitalDetailView.as_view(), name='social_capital_detail'),
]


