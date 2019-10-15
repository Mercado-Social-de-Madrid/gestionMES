
from django.conf.urls import url

from . import views

app_name='balance'

urlpatterns = [
    url(r'^badge/create$', views.NewSocialBadge.as_view(), name='create_badge'),
    url(r'^badge/(?P<pk>\d+)/$', views.SocialBadgeDetailView.as_view(), name='badge_detail'),
]


