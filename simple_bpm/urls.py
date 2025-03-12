
from django.urls import path

from . import views


app_name = 'bpm'

urlpatterns = [

    path('', views.ProcessesListView.as_view(), name='list'),
    path('process/add/', views.ProcessCreateView.as_view(), name='add'),
    path('process/<int:pk>/', views.ProcessDetailView.as_view(), name='detail'),
    path('process/<int:pk>/delete/', views.delete_process, name='delete'),

    path('workflow/add_event/', views.AddWorkflowEventView.as_view(), name='add_workflow_event'),
    path('workflow/revert_step/', views.revert_step, name='revert_step'),
]


