
from django.conf.urls import url

from . import views


app_name = 'bpm'

urlpatterns = [

    url(r'^$', views.ProcessesListView.as_view(), name='list'),
    url(r'^process/add/$', views.ProcessCreateView.as_view(), name='add'),
    url(r'^process/(?P<pk>\d+)/$', views.ProcessDetailView.as_view(), name='detail'),
    url(r'^process/(?P<pk>\d+)/delete/$', views.delete_process, name='delete'),

    url(r'^workflow/add_event/$', views.AddWorkflowEventView.as_view(), name='add_workflow_event'),
    url(r'^workflow/revert_step/$', views.revert_step, name='revert_step'),
]


