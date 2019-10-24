
from django.conf.urls import url

from . import views

app_name='balance'

urlpatterns = [
    url(r'^badges/$', views.BadgesListView.as_view(), name='badge_list'),
    url(r'^badges/create$', views.NewSocialBadge.as_view(), name='create_badge'),
    url(r'^badges/(?P<pk>\d+)/$', views.SocialBadgeDetailView.as_view(), name='badge_detail'),
    url(r'^badges/(?P<pk>\d+)/edit/$', views.SocialBadgeEditView.as_view(), name='badge_edit'),
    url(r'^render/(?P<pk>\d+)/$', views.SocialBadgeRender.as_view(), name='badge_render'),
]


