# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.models import Provider, ACTIVE
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin


class CatalogFilterForm(BootstrapForm):
    field_order = ['search', 'categories', ]


class CatalogFilter(django_filters.FilterSet):

    search = SearchFilter(names=['address', 'name', 'business_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))

    class Meta:
        model = Provider
        form = CatalogFilterForm
        fields = { 'categories':['exact'] }


class CatalogListView(FilterMixin, FilterView, AjaxTemplateResponseMixin):

    queryset = Provider.objects.filter(status=ACTIVE).prefetch_related('social_balances')
    template_name = 'catalog/list.html'
    ajax_template_name = 'catalog/query.html'
    filterset_class = CatalogFilter
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        context['hide_navbar'] = True
        return context