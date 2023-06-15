
from django.conf.urls import url

from . import views

app_name='balance'

urlpatterns = [
    url(r'^balance/badges/$', views.BadgesListView.as_view(), name='badge_list'),
    url(r'^balance/badges/create$', views.NewSocialBadge.as_view(), name='create_badge'),
    url(r'^balance/badges/(?P<pk>\d+)/$', views.SocialBadgeDetailView.as_view(), name='badge_detail'),
    url(r'^balance/badges/(?P<pk>\d+)/edit/$', views.SocialBadgeEditView.as_view(), name='badge_edit'),
    url(r'^balance/render/(?P<pk>\d+)/$', views.SocialBadgeRender.as_view(), name='badge_render'),

    url(r'^balance/$', views.SocialBalanceYear.as_view(), name='balance'),
    url(r'^balance/(?P<year>\d+)/$', views.SocialBalanceYear.as_view(), name='balance_year'),
    url(r'^accounts/providers/(?P<entity_pk>\d+)/balance/(?P<year>\d+)/$', views.SocialBalanceEditView.as_view(), name='entity_year'),
    url(r'^accounts/providers/(?P<entity_pk>\d+)/balance/(?P<year>\d+)/renderbadge/$', views.generate_badge, name='generate_badge'),

    url(r'^balance/import/$', views.ImportSocialBalanceFormView.as_view(), name='bulk_import'),

    url(r'^balance/processes/$', views.BalanceProcessList.as_view(), name='process_list'),
    url(r'^balance/processes/generate/$', views.BalanceProcessGenerate.as_view(), name='process_generate'),
    url(r'^balance/processes/year/(?P<year_create>\d+)/$', views.BalanceProcessList.as_view(), name='process_list_year'),
    url(r'^balance/processes/(?P<pk>\d+)/$', views.BalanceProcessDetail.as_view(), name='process_detail'),
    url(r'^balance/processes/cancel/$', views.cancel, name='cancel_process'),
]


