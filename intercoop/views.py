# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, ListView
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget
from filters.views import FilterMixin

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.TabbedViewMixin import TabbedViewMixin
from intercoop.forms.account import IntercoopAccountForm, IntercoopAccountSignupForm
from intercoop.forms.entity import IntercoopEntityForm
from intercoop.models import IntercoopAccount, IntercoopEntity


class  IntercoopAccountFilterForm(BootstrapForm):
    field_order = ['o', 'search', ]


class IntercoopAccountFilter(django_filters.FilterSet):

    search = SearchFilter(names=['first_name', 'last_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'registration_date', 'expiration_date'], field_labels={'name':'Nombre', 'registration_date':'Fecha de registro', 'expiration_date':'Fecha de expiración'})
    validated = django_filters.BooleanFilter(field_name='validated',
                                             widget=BooleanWidget(attrs={'class': 'threestate'}))


    class Meta:
        model = IntercoopAccount
        form = IntercoopAccountFilterForm
        fields = { 'entity':['exact']}




class IntercoopAccountsList(PermissionRequiredMixin, FilterMixin, ExportAsCSVMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'intercoop.mespermission_can_view_accounts'
    model = IntercoopAccount
    queryset = IntercoopAccount.objects.all().order_by('-registration_date')
    objects_url_name = 'account_detail'
    template_name = 'intercoop/account/list.html'
    ajax_template_name = 'intercoop/account/query.html'
    filterset_class = IntercoopAccountFilter
    paginate_by = 15

    csv_filename = 'intercoop'
    available_fields = ['cif', 'entity', 'first_name', 'last_name', 'contact_email',
                        'registration_date', 'contact_phone', ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entities'] = IntercoopEntity.objects.all()

        return context


class EntityList(PermissionRequiredMixin, ExportAsCSVMixin, ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'intercoop.mespermission_can_manage_entity'
    model = IntercoopEntity
    queryset = IntercoopEntity.objects.all()
    objects_url_name = 'entity_detail'
    template_name = 'intercoop/entity/list.html'
    ajax_template_name = 'intercoop/entity/query.html'
    paginate_by = 15

    csv_filename = 'intercoop'
    available_fields = ['cif', 'entity', 'first_name', 'last_name', 'contact_email',
                        'registration_date', 'contact_phone', ]



class EntityCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'intercoop.mespermission_can_add_entity'
    form_class = IntercoopEntityForm
    model = IntercoopEntity
    template_name = 'intercoop/entity/create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Entidad añadida correctamente.'))
        return response

    def get_success_url(self):
        return reverse('intercoop:entity_list')


class EntityDetail(PermissionRequiredMixin, UpdateView):
    permission_required = 'intercoop.mespermission_can_manage_entity'
    template_name = 'intercoop/entity/detail.html'
    form_class = IntercoopEntityForm
    model = IntercoopEntity

    def get_success_url(self):
        return reverse('intercoop:entity_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return response


class AccountSlugCreate(CreateView):

    form_class = IntercoopAccountSignupForm
    model = IntercoopAccount
    template_name = 'intercoop/account/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entity_slug = self.kwargs['slug']
        context['entity'] = IntercoopEntity.objects.filter(slug=entity_slug).first()

        return context

    def get_initial(self):
        entity_slug = self.kwargs['slug']
        entity = IntercoopEntity.objects.filter(slug=entity_slug).first()
        return {
            'entity': entity,
            'active': False
        }

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Entidad añadida correctamente.'))
        return response

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(self.request, _('Usuario añadido correctamente.'))
            return reverse('intercoop:signup_list')
        else:
            return reverse('accounts:signup_success')


class AccountDetail(TabbedViewMixin, UpdateView):
    template_name = 'intercoop/account/detail.html'
    form_class = IntercoopAccountForm
    default_tab = 'details'
    available_tabs = ['details', 'payments', 'currency']
    model = IntercoopAccount

    def get_success_url(self):
        return reverse('intercoop:account_detail', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        response = super().form_invalid(form)
        print(form.errors)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(self.request, _('Datos actualizados correctamente.'))
        return response


def validate_account(request, pk):
    if request.method == "POST":
        account = IntercoopAccount.objects.get(pk=pk)
        account.validate_account()
        return redirect(reverse('intercoop:account_detail', kwargs={'pk': account.pk}))

    return False
