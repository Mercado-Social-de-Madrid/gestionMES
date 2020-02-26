
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView
from django_filters.views import FilterView
from filters.views import FilterMixin
from accounts.models import Account
from accounts.forms.provider import ProviderForm, ProviderSignupForm
from accounts.mixins.feecomments import FeeCommentsMixin
from accounts.mixins.signup import SignupFormMixin
from accounts.models import Provider, SignupProcess, Category, ACTIVE
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.TabbedViewMixin import TabbedViewMixin
from core.mixins.XFrameExemptMixin import XFrameOptionsExemptMixin
from payments.models import FeeRange, PendingPayment
from social_balance.models import EntitySocialBalance, SocialBalanceBadge

class AccountFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class AccountFilter(django_filters.FilterSet):

    # search = SearchFilter(names=['address', 'name', 'business_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'registration_date'], field_labels={'name':'Nombre', 'registration_date':'Fecha de alta'})

    class Meta:
        model = Account
        form = AccountFilterForm
        fields = { 'status':['exact'], }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.initial['status'] = ACTIVE


class AccountListView(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = Account
    queryset = Account.objects.all().prefetch_related('app_user')
    objects_url_name = 'provider_detail'
    template_name = 'account/list.html'
    ajax_template_name = 'account/results.html'
    filterset_class = AccountFilter
    paginate_by = 15

