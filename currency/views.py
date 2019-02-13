# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.forms.process import SignupProcessForm
from accounts.models import SignupProcess
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from currency.forms.guest import GuestAccountForm
from currency.forms.invite import GuestInviteForm
from currency.models import GuestInvitation, GuestAccount
from mes import settings
from payments.models import PendingPayment
from simple_bpm.custom_filters import WorkflowFilter
from simple_bpm.forms.WorkflowEventForm import WorkflowEventForm


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


class NewInvite(CreateView):

    form_class = GuestInviteForm
    model = GuestAccount
    template_name = 'invite/create.html'

    def get_initial(self):
        return {'invite_token': self.kwargs.get('uuid')}

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        uuid = self.kwargs.get('uuid')
        if not GuestInvitation.objects.is_valid_token(uuid):
            raise Http404("Token de invitación no válido")

        return super(NewInvite, self).dispatch(request, *args, **kwargs)

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





