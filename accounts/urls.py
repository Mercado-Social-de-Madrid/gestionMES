
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^categories/$', views.CategoryListView.as_view(), name='category_list'),
    url(r'^categories/add/$', views.CategoryCreate.as_view(), name='add_category'),
    url(r'^categories/(?P<pk>[0-9a-f-]+)/$', views.CategoryDetailView.as_view(), name='category_detail'),

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
]


