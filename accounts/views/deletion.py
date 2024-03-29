# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django_filters.views import FilterView

from accounts.models import SignupProcess, Account, DeletionProcess
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers import FilterMixin
from simple_bpm.custom_filters import WorkflowFilter
from simple_bpm.forms.WorkflowEventForm import WorkflowEventForm
from simple_bpm.views import cancel_process


class DeletionFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class DeletionFilter(django_filters.FilterSet):

    search = SearchFilter(names=['name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'last_update'], field_labels={'name':'Nombre', 'last_update':'Última actualización'})
    status = WorkflowFilter(['account_deletion'], label='Estado')

    class Meta:
        model = SignupProcess
        form = DeletionFilterForm
        fields = { 'member_type':['exact'], }


class DeletionListView(PermissionRequiredMixin, FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'accounts.mespermission_can_view_deletions'
    queryset = DeletionProcess.objects.pending().order_by('-last_update')
    objects_url_name = 'deletion_detail'
    template_name = 'deletion/list.html'
    ajax_template_name = 'deletion/query.html'
    filterset_class = DeletionFilter
    paginate_by = 15


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


def delete_account(request, pk):
    if request.method == "POST":
        account = Account.objects.get(pk=pk)
        process = DeletionProcess.objects.create_process(account=account)
        return redirect(reverse('accounts:deletion_detail', kwargs={'pk': process.pk}))

    return False


def cancel_delete(request):
    return cancel_process(request, DeletionProcess)


def revert_delete(request):
    if request.method == "POST":
        redirect_url = request.POST.get('redirect_to', '')
        process_pk = request.POST.get('process', None)

        if redirect_url and process_pk:
            process = DeletionProcess.objects.filter(pk=process_pk).first()
            if process:
                process.revert()
            return redirect(redirect_url)

    return False