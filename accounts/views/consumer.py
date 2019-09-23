# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import csv

import datetime
import django_filters
import polymorphic
from django.contrib import messages
from django.core.exceptions import FieldDoesNotExist
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.forms.consumer import ConsumerForm, ConsumerSignupForm
from accounts.models import Consumer, SignupProcess
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.TabbedViewMixin import TabbedViewMixin
from core.mixins.XFrameExemptMixin import XFrameOptionsExemptMixin
from payments.models import PendingPayment


class ConsumerFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class ConsumerFilter(django_filters.FilterSet):

    search = SearchFilter(names=['address', 'first_name', 'last_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['last_name', 'registration_date'])

    class Meta:
        model = Consumer
        form = ConsumerFilterForm
        fields = { 'status':['exact'], }


class ConsumersListView(FilterMixin, ExportAsCSVMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = Consumer
    queryset = Consumer.objects.all()
    objects_url_name = 'consumer_detail'
    template_name = 'consumer/list.html'
    ajax_template_name = 'consumer/query.html'
    filterset_class = ConsumerFilter
    paginate_by = 15

    csv_filename = 'consumidoras'
    available_fields = ['cif', 'first_name', 'last_name', 'address', 'display_name', 'contact_email', 'contact_phone',
                        'postalcode', 'city', 'address', 'province', 'iban_code', 'registration_date',]
    field_labels = {'display_name': 'Nombre completo'}


class ConsumerSignup(XFrameOptionsExemptMixin, CreateView):

    form_class = ConsumerSignupForm
    model = Consumer
    template_name = 'consumer/create.html'

    def form_valid(self, form):
        super(ConsumerSignup, self).form_valid(form)
        SignupProcess.objects.create_process(account=self.object)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(self.request, _('Usuario añadido correctamente.'))
            return reverse('accounts:signup_list')
        else:
            process = SignupProcess.objects.filter(account=self.object).first()
            if process and process.should_show_payment():
                payment = PendingPayment.objects.filter(account=self.object).first()
                return reverse('accounts:signup_success')+'?payment='+payment.uuid
            else:
                return reverse('accounts:signup_success')



class ConsumerUpdateView(UpdateView):
    template_name = 'consumer/edit.html'
    form_class = ConsumerSignupForm
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
        if process != None:
            account = process.account
            if account:
                account.process = process
            return account


class ConsumerDetailView(TabbedViewMixin, UpdateView):
    template_name = 'consumer/detail.html'
    default_tab = 'details'
    available_tabs = ['details', 'payments', 'currency']
    form_class = ConsumerForm
    model = Consumer

    def get_success_url(self):
        return reverse('accounts:consumer_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super(ConsumerDetailView, self).form_valid(form)
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return response

    def get_context_data(self, **kwargs):
        context = super(ConsumerDetailView, self).get_context_data(**kwargs)

        context['payments'] = PendingPayment.objects.filter(account=self.object)
        context['profile_tab'] = True
        context['signup'] = self.object.signup_process.first()
        return context

