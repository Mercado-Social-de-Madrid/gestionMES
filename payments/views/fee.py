# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import django_filters
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.management import call_command
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import formats
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import UpdateView
from django_filters.views import FilterView
from django_filters.widgets import BooleanWidget
from helpers import FilterMixin

from accounts.custom_filters import AccountSearchFilter, CollaborationFilter
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.FormsetView import FormsetView
from payments.forms.FeeComment import FeeCommentForm
from payments.forms.feecharge import getFeeSplitFormset, AccountFeeSplitForm
from payments.models import AccountAnnualFeeCharge, AnnualFeeCharges, PendingPayment


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
        try:
           annualFee = AnnualFeeCharges.objects.get(year=year)
        except AnnualFeeCharges.DoesNotExist:
            raise Http404
        # Disable automatic generation of pending payments (https://trello.com/c/0ng43qhW/6-1-hay-pagos-que-se-crean-automaticamente)
        # if not 'page' in self.request.GET and not self.request.is_ajax():
        #     annualFee.create_pending_data()
        #     if created:
        #         messages.success(self.request, _('Proceso anual de cobro creado correctamente.'))

        return annualFee.accountannualfeecharge_set.all()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_amount'] = self.object_list.aggregate(sum=Sum('payment__amount'))['sum']
        context['years'] = AnnualFeeCharges.objects.values_list('year', flat=True)
        context['current_year'] = int(self.kwargs.get('year'))
        context['current_month'] = formats.date_format(datetime.now(), format='F').lower()
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


class SplitFeeCharge(UpdateView, FormsetView):

    model = AccountAnnualFeeCharge
    form_class = AccountFeeSplitForm
    template_name = 'fee/split.html'

    def get_named_formsets(self):
        return{ 'split': getFeeSplitFormset(initial=True) }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = int(self.kwargs.get('year'))
        return context

    def get_success_url(self):
        return reverse('payments:annual_feecharges', kwargs={'year': int(self.kwargs.get('year'))})

    def formset_split_valid(self, splits, annualcharge):

        annualcharge.split = True
        for payment in annualcharge.payments.all():
            payment.delete()

        for split in splits:
            payment = PendingPayment.objects.create(
                        concept=split.cleaned_data['concept'],
                        account=annualcharge.account,
                        amount= split.cleaned_data['amount'])
            print(split.cleaned_data['date'])
            payment.added = split.cleaned_data['date']
            payment.save()
            annualcharge.payments.add(payment)
            annualcharge.save()

    def post_form_valid(self, form):
        if self.object.payments.count() > 0:
            # If we split the annual charge, we need to remove the unique one
            if self.object.payment:
                self.object.payment.delete()
                self.object.payment = None
            self.object.split = True

        fee = form.cleaned_data['new_amount']
        if self.object.amount != fee:
            self.object.amount = fee
            self.object.manually_modified = True

        self.object.save()


class GenerateFeesView(View):

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            year = datetime.now().year

            if request.POST.get("type") == "month":
                call_command('generate_consumers_annual_fee_by_month', user=request.user, year=year)
            elif request.POST.get("type") == "year":
                call_command('generate_consumers_annual_fee', user=request.user, year=year)

            return redirect(reverse('payments:annual_feecharges', kwargs={"year": year}))
