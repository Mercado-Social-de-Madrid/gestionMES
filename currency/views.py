# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import CreateView, UpdateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.models import Account
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.XFrameExemptMixin import XFrameOptionsExemptMixin
from currency.forms.guest import GuestAccountForm
from currency.forms.invite import GuestInviteForm
from currency.models import GuestInvitation, GuestAccount, CurrencyAppUser


class  InvitesFilterForm(BootstrapForm):
    field_order = ['o', 'search', ]


class InvitesFilter(django_filters.FilterSet):

    search = SearchFilter(names=['first_name', 'last_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'registration_date', 'expiration_date'], field_labels={'name':'Nombre', 'registration_date':'Fecha de registro', 'expiration_date':'Fecha de expiración'})

    class Meta:
        model = GuestAccount
        form = InvitesFilterForm
        fields = { 'active':['exact'], }

class InvitesListView(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = GuestAccount.objects.all().order_by('-registration_date')
    objects_url_name = 'guest_detail'
    template_name = 'invite/list.html'
    ajax_template_name = 'invite/query.html'
    filterset_class = InvitesFilter
    paginate_by = 15


class NewInvite(XFrameOptionsExemptMixin, CreateView):

    form_class = GuestInviteForm
    model = GuestAccount
    template_name = 'invite/create.html'

    def get_initial(self):
        return {'invite_token': self.kwargs.get('uuid')}

    def get_context_data(self, **kwargs):
        uuid = self.kwargs.get('uuid')
        context = super(NewInvite, self).get_context_data(**kwargs)
        if not GuestInvitation.objects.is_valid_token(uuid):
            context['invalid_token'] = True

        return context

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(self.request, _('Proceso de acogida añadido correctamente.'))
            return reverse('currency:guest_user_list')
        else:
            return reverse('currency:invite_success')


class GuestAccountDetailView(UpdateView):
    template_name = 'invite/detail.html'
    queryset = GuestAccount.objects.all()
    model = GuestAccount
    form_class = GuestAccountForm


    def get_success_url(self):
        return reverse('accounts:signup_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(GuestAccountDetailView, self).get_context_data(**kwargs)

        return context

def add_app_user(request):

    if request.method == "POST":
        redirect_url = request.POST.get('redirect_to', '')
        account_pk = request.POST.get('account', None)

        if redirect_url and account_pk:
            account = Account.objects.filter(pk=account_pk).first()
            if account:
                CurrencyAppUser.objects.create_app_user(account)

            return redirect(redirect_url)

    return False

#



