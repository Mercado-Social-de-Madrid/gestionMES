
from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.ProcessesListView.as_view(), name='list'),
    url(r'^process/add/$', views.ProcessCreateView.as_view(), name='add'),
    url(r'^process/(?P<pk>\d+)/$', views.ProcessDetailView.as_view(), name='detail'),

    url(r'^workflow/add_event/$', views.add_workflow_event, name='add_workflow_event'),
]


