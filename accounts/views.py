# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView, DetailView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.forms.category import CategoryForm
from accounts.forms.consumer import ConsumerForm
from accounts.forms.process import SignupProcessForm
from accounts.forms.provider import ProviderForm
from accounts.models import Provider, Consumer, SignupProcess, Category
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.forms.password import PasswordForm
from core.forms.profile import ProfileForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.TabbedViewMixin import TabbedViewMixin
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


class ProvidersListView(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = Provider.objects.all()
    objects_url_name = 'provider_detail'
    template_name = 'provider/list.html'
    ajax_template_name = 'provider/query.html'
    filterset_class = ProviderFilter
    paginate_by = 15


class ProviderDetailView(TabbedViewMixin, UpdateView):
    template_name = 'provider/detail.html'
    default_tab = 'details'
    available_tabs = ['details', 'payments']
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

        context['payments'] = PendingPayment.objects.filter(account=self.object)
        context['profile_tab'] = True
        return context



class ConsumerFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class ConsumerFilter(django_filters.FilterSet):

    search = SearchFilter(names=['address', 'first_name', 'last_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['last_name', 'registration_date'])

    class Meta:
        model = Consumer
        form = ConsumerFilterForm
        fields = { 'status':['exact'], }


class ConsumersListView(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = Consumer.objects.all()
    objects_url_name = 'consumer_detail'
    template_name = 'consumer/list.html'
    ajax_template_name = 'consumer/query.html'
    filterset_class = ConsumerFilter
    paginate_by = 15


class ProviderSignup(CreateView):

    form_class = ProviderForm
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

        return context

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(self.request, _('Proceso de acogida añadido correctamente.'))
            return reverse('accounts:signup_list')
        else:
            return reverse('accounts:signup_success')

class ConsumerSignup(CreateView):

    form_class = ConsumerForm
    model = Consumer
    template_name = 'consumer/create.html'

    def form_valid(self, form):
        response = super(ConsumerSignup, self).form_valid(form)
        SignupProcess.objects.create_process(account=self.object)

        return response

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(self.request, _('Usuario añadido correctamente.'))
            return reverse('accounts:signup_list')
        else:
            return reverse('accounts:signup_success')


class SignupFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class SignupFilter(django_filters.FilterSet):

    search = SearchFilter(names=['name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'last_update'], field_labels={'name':'Nombre', 'last_update':'Última actualización'})
    status = WorkflowFilter(['prov_signup'], label='Estado')

    class Meta:
        model = SignupProcess
        form = SignupFilterForm
        fields = { 'member_type':['exact'], }


class SignupListView(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = SignupProcess.objects.pending().order_by('-last_update')
    objects_url_name = 'signup_detail'
    template_name = 'signup/list.html'
    ajax_template_name = 'signup/query.html'
    filterset_class = SignupFilter
    paginate_by = 15


class NewSignup(CreateView):

    form_class = SignupProcessForm
    model = SignupProcess
    template_name = 'signup/create.html'

    def form_valid(self, form):
        response = super(NewSignup, self).form_valid(form)
        self.object.initialize()
        return response

    def get_success_url(self):
        messages.success(self.request, _('Proceso de acogida añadido correctamente.'))
        return reverse('accounts:signup_list')


class SignupDetailView(DetailView):
    template_name = 'signup/detail.html'
    queryset = SignupProcess.objects.all()
    model = SignupProcess

    def get_success_url(self):
        return reverse('accounts:signup_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(SignupDetailView, self).get_context_data(**kwargs)

        if self.object.workflow.is_first_step():
            context['first_step'] = True

        if self.object.is_in_payment_step():
            context['payment_step'] = True
            context['payment'] = PendingPayment.objects.filter(account=self.object.account).first()

        form = WorkflowEventForm(initial={
            'workflow':context['object'].workflow,
            'redirect_to': reverse('accounts:signup_detail', kwargs={'pk': self.object.pk})
        })
        context['comment_form'] = form
        return context


def signup_form_redirect(request, uuid):

    process = SignupProcess.objects.filter(uuid=uuid).first()
    if process.member_type == settings.MEMBER_PROV:
        return redirect('accounts:provider_edit_form',uuid=uuid )

    elif process.member_type == settings.MEMBER_CONSUMER:
        return redirect('accounts:consumer_edit_form', uuid=uuid )


class ProviderUpdateView(UpdateView):
    template_name = 'provider/edit.html'
    form_class = ProviderForm
    model = Provider

    def getSignup(self):
        uuid = self.kwargs.get('uuid')
        process = SignupProcess.objects.filter(uuid=uuid).first()
        if not process:
            raise Http404("No se encontró el proceso")
        else:
            return process

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(self.request, _('Proceso de acogida añadido correctamente.'))
            return reverse('accounts:signup_detail', kwargs={'pk': self.getSignup().pk})
        else:
            return reverse('accounts:signup_success')

    def form_valid(self, form):
        response = super(ProviderUpdateView, self).form_valid(form)
        process = self.getSignup()
        process.form_filled(self.object)
        return response

    def get_object(self, queryset=None):

        process = self.getSignup()
        if process != None: #and process.member_type == :
            account = process.account
            return account


class ConsumerUpdateView(UpdateView):
    template_name = 'consumer/edit.html'
    form_class = ConsumerForm
    model = Consumer

    def getSignup(self):
        uuid = self.kwargs.get('uuid')
        process = SignupProcess.objects.filter(uuid=uuid).first()
        if not process:
            raise Http404("No se encontró el proceso")
        else:
            return process

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(self.request, _('Proceso de acogida añadido correctamente.'))
            return reverse('accounts:signup_detail', kwargs={'pk': self.getSignup().pk})
        else:
            return reverse('accounts:signup_success')

    def form_valid(self, form):
        response = super(ConsumerUpdateView, self).form_valid(form)
        process = self.getSignup()
        process.form_filled(self.object)
        return response

    def get_object(self, queryset=None):

        process = self.getSignup()
        if process != None: #and process.member_type == :
            account = process.account
            return account



class CategoryListView(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = Category.objects.all()
    model = Category
    objects_url_name = 'category_detail'
    template_name = 'category/list.html'
    ajax_template_name = 'category/query.html'
    paginate_by = 15


class CategoryCreate(CreateView):

    form_class = CategoryForm
    model = Category
    template_name = 'category/create.html'

    def form_valid(self, form):
        response = super(CategoryCreate, self).form_valid(form)
        messages.success(self.request, _('Categoría añadida correctamente.'))
        return response

    def get_success_url(self):
        return reverse('accounts:category_list')


class CategoryDetailView(UpdateView):
    template_name = 'category/detail.html'
    form_class = CategoryForm
    model = Category

    def get_success_url(self):
        return reverse('accounts:category_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super(CategoryDetailView, self).form_valid(form)
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return response
