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


class ProviderFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class ProviderFilter(django_filters.FilterSet):

    search = SearchFilter(names=['address', 'name', 'business_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'start_year', 'registration_date'], field_labels={'name':'Nombre', 'start_year':'Año de inicio', 'registration_date':'Fecha de alta'})

    class Meta:
        model = Provider
        form = ProviderFilterForm
        fields = { 'status':['exact'], }


class ProvidersListView(FilterMixin, ExportAsCSVMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = Provider
    queryset = Provider.objects.all()
    objects_url_name = 'provider_detail'
    template_name = 'provider/list.html'
    ajax_template_name = 'provider/query.html'
    filterset_class = ProviderFilter
    paginate_by = 15

    csv_filename = 'proveedoras'
    available_fields = ['cif', 'name', 'business_name', 'public_address', 'address',  'contact_email', 'contact_phone',
                        'postalcode', 'city', 'address', 'province', 'iban_code', 'registration_date', 'is_physical_store',
                        'bonus_percent_entity', 'bonus_percent_general', 'max_percent_payment', 'start_year']


class ProviderDetailView(TabbedViewMixin, UpdateView):
    template_name = 'provider/detail.html'
    default_tab = 'details'
    available_tabs = ['details', 'payments', 'currency']
    form_class = ProviderForm
    model = Provider

    def get_success_url(self):
        return reverse('accounts:provider_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super(ProviderDetailView, self).form_valid(form)
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return response

    def get_context_data(self, **kwargs):
        context = super(ProviderDetailView, self).get_context_data(**kwargs)

        context['fee'] = FeeRange.calculate_fee(self.object)
        context['categories'] = Category.objects.all()
        context['payments'] = PendingPayment.objects.filter(account=self.object)
        context['signup'] = self.object.signup_process.first()
        print self.object.signup_process.all()
        context['profile_tab'] = True

        return context

class ProviderSignup(XFrameOptionsExemptMixin, CreateView):

    form_class = ProviderSignupForm
    model = Provider
    template_name = 'provider/create.html'

    def form_valid(self, form):
        response = super(ProviderSignup, self).form_valid(form)
        SignupProcess.objects.create_process(account=self.object)

        return response


    def get_context_data(self, **kwargs):
        context = super(ProviderSignup, self).get_context_data(**kwargs)

        context['worker_ranges'] = FeeRange.objects.order_by('min_num_workers').values('min_num_workers', 'max_num_workers').distinct()
        context['income_ranges'] = FeeRange.objects.order_by('min_income').values('min_income', 'max_income').distinct()
        context['fees'] = FeeRange.objects.all()
        context['categories'] = Category.objects.all()

        return context

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(self.request, _('Proceso de acogida añadido correctamente.'))
            return reverse('accounts:signup_list')
        else:
            return reverse('accounts:signup_success')

class ProviderUpdateView(UpdateView):
    template_name = 'provider/edit.html'
    form_class = ProviderSignupForm
    model = Provider

    def getSignup(self):
        uuid = self.kwargs.get('uuid')
        process = SignupProcess.objects.filter(uuid=uuid).first()
        if not process:
            raise Http404("No se encontró el proceso")
        else:
            return process

    def get_success_url(self):
        messages.success(self.request, _('Proceso de acogida actualizado correctamente.'))
        if self.request.user.is_authenticated:
            return reverse('accounts:signup_detail', kwargs={'pk': self.getSignup().pk})
        else:
            return reverse('accounts:signup_success')

    def get_context_data(self, **kwargs):
        context = super(ProviderUpdateView, self).get_context_data(**kwargs)

        context['worker_ranges'] = FeeRange.objects.order_by('min_num_workers').values('min_num_workers', 'max_num_workers').distinct()
        context['income_ranges'] = FeeRange.objects.order_by('min_income').values('min_income', 'max_income').distinct()
        context['fees'] = FeeRange.objects.all()
        context['categories'] = Category.objects.all()

        return context

    def form_valid(self, form):
        response = super(ProviderUpdateView, self).form_valid(form)
        process = self.getSignup()
        process.form_filled(self.object)
        return response

    def get_initial(self):
        initial = super(ProviderUpdateView, self).get_initial()
        initial['check_privacy_policy'] = True
        initial['check_conditions'] = True
        return initial

    def get_object(self, queryset=None):
        process = self.getSignup()
        if process != None:
            account = process.account
            if account:
                account.process = process
            return account
