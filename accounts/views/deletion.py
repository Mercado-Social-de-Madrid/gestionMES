# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import CreateView, DetailView, TemplateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.forms.process import SignupProcessForm
from accounts.models import SignupProcess, Account, DeletionProcess
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from mes import settings
from payments.models import PendingPayment
from simple_bpm.custom_filters import WorkflowFilter
from simple_bpm.forms.WorkflowEventForm import WorkflowEventForm


def delete_account(request, pk):
    if request.method == "POST":
        account = Account.objects.get(pk=pk)
        process = DeletionProcess.objects.create_process(account=account)
        return redirect(reverse('accounts:deletion_detail', kwargs={'pk': process.pk}))

    return False

class DeletionDetailView(DetailView):
    template_name = 'deletion/detail.html'
    queryset = DeletionProcess.objects.all()
    model = DeletionProcess

    def get_success_url(self):
        return reverse('accounts:signup_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(DeletionDetailView, self).get_context_data(**kwargs)

        if self.object.workflow.is_first_step():
            context['first_step'] = True

        form = WorkflowEventForm(initial={
            'workflow':context['object'].workflow,
            'redirect_to': reverse('accounts:deletion_detail', kwargs={'pk': self.object.pk})
        })
        context['comment_form'] = form
        return context