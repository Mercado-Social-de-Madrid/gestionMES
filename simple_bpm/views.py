# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, DetailView
from django_filters.views import FilterView
from filters.views import FilterMixin

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.FormsetView import FormsetView
import core.forms
from core.mixins.ListItemUrlMixin import ListItemUrlMixin

from simple_bpm.forms.WorkflowEventForm import WorkflowEventForm
from simple_bpm.forms.process import ProcessForm, getStepsFormset
from simple_bpm.models import Process, ProcessStepTask


class FilterForm(BootstrapForm):
    field_order = ['o', 'title', 'member_type', ]

class ProcessFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Buscar...')
    o = LabeledOrderingFilter(fields=['title', 'created'])

    class Meta:
        model = Process
        form = FilterForm
        fields = { 'member_type':['exact'], }


class ProcessesListView(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = Process.objects.all()
    objects_url_name = 'detail'
    model = Process
    template_name = 'bpm/list.html'
    ajax_template_name = 'bpm/query.html'
    filterset_class = ProcessFilter
    paginate_by = 10


class ProcessCreateView(CreateView, FormsetView):
    model = Process
    form_class = ProcessForm
    template_name = 'bpm/create.html'


    def get_success_url(self):
        return reverse('bpm:list')


    def get_named_formsets(self):
        return{
            'steps': getStepsFormset(initial=True)
        }

    def formset_steps_valid(self, steps, process):

        for step in steps:
            process_step = step.save(commit=False)
            process_step.process = process
            process_step.save()

            if 'checklist_tasks' in step.cleaned_data:
                checklist_items = step.cleaned_data.get('checklist_tasks')
                checklist = checklist_items.split(settings.INLINE_INPUT_SEPARATOR)

                print(process_step.pk)

                for order, description in enumerate(checklist, start=1):
                    if not description:
                        continue
                    task = ProcessStepTask()
                    task.process_step = process_step
                    task.description = description
                    task.save()


class ProcessDetailView(DetailView):
    model = Process
    template_name = 'bpm/detail.html'



def add_workflow_event(request):

    if request.method == "POST":
        form = WorkflowEventForm(request.POST,)
        if form.is_valid():
            redirect_url = form.cleaned_data['redirect_to']
            event = form.save(commit=False)

            if 'add_comment' in request.POST:
                event.workflow.add_comment(request.user, form.cleaned_data['comment'])
            else:
                event.workflow.complete_current_step(request.user)

        return redirect(redirect_url)
    else:
        return False


