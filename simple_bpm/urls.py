
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.ProcessesListView.as_view(), name='list'),
    url(r'^process/(?P<pk>\d+)/$', views.ProcessDetailView.as_view(), name='detail'),
]


