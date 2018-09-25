# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django import forms
from django_filters.views import FilterView
from django.shortcuts import render
from django.views.generic import ListView
from filters.views import FilterMixin

from core.forms.BootstrapModelForm import BootstrapModelForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from simple_bpm.models import Process



class FilterForm(BootstrapModelForm):
    field_order = ['title', 'member_type', ]

class ProcessFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Buscar...')

    class Meta:
        model = Process
        form = FilterForm
        fields = {
            'member_type':['exact'],
        }



class ProcessesListView(FilterMixin, FilterView, AjaxTemplateResponseMixin):
    model = Process
    template_name = 'bpm/list.html'
    ajax_template_name = 'bpm/query.html'
    filterset_class = ProcessFilter
    paginate_by = 2



def register(request):

    processes = Process.objects.all()
    return render(request, 'registration/signup.html', {'processes': processes})

