# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django_filters.views import FilterView
from filters.views import FilterMixin

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.forms.BootstrapModelForm import BootstrapModelForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from simple_bpm.models import Process


class FilterForm(BootstrapModelForm):
    field_order = ['o', 'title', 'member_type', ]

class ProcessFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Buscar...')
    o = LabeledOrderingFilter(fields=['title', 'created'])

    class Meta:
        model = Process
        form = FilterForm
        fields = { 'member_type':['exact'], }


class ProcessesListView(FilterMixin, FilterView, AjaxTemplateResponseMixin):

    queryset = Process.objects.all()
    model = Process
    template_name = 'bpm/list.html'
    ajax_template_name = 'bpm/query.html'
    filterset_class = ProcessFilter
    paginate_by = 10


