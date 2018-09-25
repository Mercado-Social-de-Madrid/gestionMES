# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django_filters.views import FilterView
from filters.views import FilterMixin

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapModelForm import BootstrapModelForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.models import User


class UserForm(BootstrapModelForm):
    field_order = ['o', 'search', 'is_active', ]


class UserFilter(django_filters.FilterSet):

    search = SearchFilter(names=['username', 'first_name', 'last_name', 'email'], lookup_expr='in')
    o = LabeledOrderingFilter(fields=['username', 'last_login', 'date_joined'])

    class Meta:
        model = User
        form = UserForm
        fields = { 'is_active':['exact'],  }


class UsersListView(FilterMixin, FilterView, AjaxTemplateResponseMixin):

    queryset = User.objects.all()
    model = User
    template_name = 'user/list.html'
    ajax_template_name = 'user/query.html'
    filterset_class = UserFilter
    paginate_by = 15


