# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import UpdateView, CreateView, DetailView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.forms.category import CategoryForm
from accounts.forms.consumer import ConsumerForm
from accounts.forms.process import SignupProcessForm
from accounts.forms.provider import ProviderForm, ProviderSignupForm
from accounts.models import Provider, Consumer, SignupProcess, Category
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.forms.password import PasswordForm
from core.forms.profile import ProfileForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.TabbedViewMixin import TabbedViewMixin
from core.mixins.XFrameExemptMixin import XFrameOptionsExemptMixin
from core.models import User
from mes import settings
from payments.models import FeeRange, PendingPayment
from simple_bpm.custom_filters import WorkflowFilter

from simple_bpm.forms.WorkflowEventForm import WorkflowEventForm

class CatalogFilterForm(BootstrapForm):
    field_order = ['search', 'categories', ]


class CatalogFilter(django_filters.FilterSet):

    search = SearchFilter(names=['address', 'name', 'business_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))

    class Meta:
        model = Provider
        form = CatalogFilterForm
        fields = { 'categories':['exact'] }


class CatalogListView(FilterMixin, FilterView, AjaxTemplateResponseMixin):

    queryset = Provider.objects.all().prefetch_related('social_balances')
    template_name = 'catalog/list.html'
    ajax_template_name = 'catalog/query.html'
    filterset_class = CatalogFilter
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super(CatalogListView, self).get_context_data(**kwargs)
        context['hide_navbar'] = True
        return context