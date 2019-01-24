# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DetailView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.forms.process import SignupProcessForm
from accounts.models import SignupProcess
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from mes import settings
from payments.models import PendingPayment
from simple_bpm.custom_filters import WorkflowFilter
from simple_bpm.forms.WorkflowEventForm import WorkflowEventForm


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

