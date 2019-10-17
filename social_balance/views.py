# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import CreateView, UpdateView, TemplateView, DetailView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.models import Account, Entity
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.XFrameExemptMixin import XFrameOptionsExemptMixin
from currency.forms.guest import GuestAccountForm
from currency.forms.invite import GuestInviteForm
from currency.models import GuestInvitation, GuestAccount, CurrencyAppUser
from social_balance.forms.badge import SocialBadgeForm
from social_balance.models import SocialBalanceBadge, EntitySocialBalance


class  InvitesFilterForm(BootstrapForm):
    field_order = ['o', 'search', ]


class InvitesFilter(django_filters.FilterSet):

    search = SearchFilter(names=['first_name', 'last_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'registration_date', 'expiration_date'], field_labels={'name':'Nombre', 'registration_date':'Fecha de registro', 'expiration_date':'Fecha de expiración'})

    class Meta:
        model = GuestAccount
        form = InvitesFilterForm
        fields = { 'active':['exact'], }

class InvitesListView(FilterMixin, ExportAsCSVMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = GuestAccount
    queryset = GuestAccount.objects.all().order_by('-registration_date')
    objects_url_name = 'guest_detail'
    template_name = 'invite/list.html'
    ajax_template_name = 'invite/query.html'
    filterset_class = InvitesFilter
    paginate_by = 15

    csv_filename = 'invitadas'
    available_fields = ['cif', 'invited_by', 'token_used', 'first_name', 'last_name', 'contact_email',
                        'registration_date', 'expiration_date', ]


class NewSocialBadge(CreateView):

    form_class = SocialBadgeForm
    model = SocialBalanceBadge
    template_name = 'social_balance/create.html'

    def get_success_url(self):
        return reverse('balance:badge_detail', kwargs={'pk': self.object.pk})



class SocialBadgeDetailView(DetailView):
    template_name = 'social_balance/detail.html'
    queryset = SocialBalanceBadge.objects.all()
    model = SocialBalanceBadge

    def get_context_data(self, **kwargs):
        context = super(SocialBadgeDetailView, self).get_context_data(**kwargs)
        return context


class SocialBadgeRender(DetailView):
    template_name = 'social_balance/render.html'
    queryset = SocialBalanceBadge.objects.all()
    model = SocialBalanceBadge

    def get_context_data(self, **kwargs):
        context = super(SocialBadgeRender, self).get_context_data(**kwargs)
        entity_id = self.request.GET.get('id', None)
        context['entity'] = Entity.objects.get(id=entity_id)
        context['balance'] = EntitySocialBalance.objects.get(entity=context['entity'], year=self.object.year)
        context['hide_navbar'] = True

        return context