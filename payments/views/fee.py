# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget
from filters.views import FilterMixin

from accounts.custom_filters import AccountSearchFilter, CollaborationFilter
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from payments.forms.FeeComment import FeeCommentForm
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges


class FeeChargeFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'account__member_type', 'uncalculated' ]


class FeeChargeFilter(django_filters.FilterSet):

    collab = CollaborationFilter(label=_('Colaboración'), collab_field='collab__collaboration')
    search = AccountSearchFilter(names=['payment__concept', 'account__cif'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['payment__amount', 'payment__added'], field_labels={'payment__amount':'Cuota', 'account__member_type':'Tipo de socia', 'payment__added':'Fecha de emisión'})
    uncalculated = django_filters.BooleanFilter(field_name='payment', lookup_expr='isnull', widget=BooleanWidget(attrs={'class':'threestate'}), label=_('Cuota sin calcular'))
    account__member_type = django_filters.ChoiceFilter(choices=settings.MEMBER_TYPES, label=_('Tipo de socia:'))
    paid = django_filters.BooleanFilter(field_name='payment__completed', widget=BooleanWidget(attrs={'class':'threestate'}), label=_('Pagado'))

    class Meta:
        model = AccountAnnualFeeCharge
        form = FeeChargeFilterForm
        fields = { 'account__member_type':['exact'] }


class AnnualFeeChargesList(PermissionRequiredMixin, FilterMixin, FilterView, ExportAsCSVMixin, AjaxTemplateResponseMixin):
    permission_required = 'payments.mespermission_can_view_payments'
    template_name = 'fee/annual.html'
    ajax_template_name = 'fee/query.html'
    filterset_class = FeeChargeFilter
    model = AccountAnnualFeeCharge
    paginate_by = 15

    csv_filename = 'cuotas'
    available_fields = ['manually_modified', 'payment__amount', 'payment__concept', 'account__display_name',
                        'payment__completed', 'payment__added', 'account__contact_phone', 'account__contact_email']
    field_labels = {'payment__amount': 'Cantidad', 'payment__concept':'Concepto', 'payment__added':'Fecha de emisión',
                    'account__display_name':'Cuenta', 'payment__completed':'Realizado',
                    'account__contact_phone':'Teléfono de contacto', 'account__contact_email': 'Email de contacto'}


    def get_queryset(self):
        year = int(self.kwargs.get('year'))
        annualFee, created = AnnualFeeCharges.objects.get_or_create(year=year)

        if not 'page' in self.request.GET and not self.request.is_ajax():
            annualFee.create_pending_data()
            if created:
                messages.success(self.request, _('Proceso anual de cobro creado correctamente.'))

        return annualFee.accountannualfeecharge_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_amount'] = self.object_list.aggregate(sum=Sum('payment__amount'))['sum']
        context['years'] = AnnualFeeCharges.objects.values_list('year', flat=True)
        context['current_year'] = int(self.kwargs.get('year'))
        return context


def add_fee_comment(request):

    if request.method == "POST":
        form = FeeCommentForm(request.POST,)
        if form.is_valid():
            redirect_url = form.cleaned_data['redirect_to']
            comment = form.save(commit=False)
            comment.completed_by = request.user
            comment.save()
            messages.success(request, _('Comentario añadido correctamente.'))
            return redirect(redirect_url)