import logging

import django_filters
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.views.generic import UpdateView
from django_filters.views import FilterView

from django.utils.translation import gettext as _
from django_filters.widgets import BooleanWidget

from accounts.custom_filters import AccountSearchFilter
from accounts.forms.social_capital import SocialCapitalForm
from accounts.models import SocialCapital
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.MemberTypeFilter import MemberTypeFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers import FilterMixin
from payments.models import PendingPayment


log = logging.getLogger(__name__)


class SocialCapitalFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class SocialCapitalFilter(django_filters.FilterSet):
    o = LabeledOrderingFilter(fields=['paid_timestamp', 'returned_timestamp'], field_labels={'paid_timestamp': 'Fecha de pago', 'returned_timestamp': 'Fecha de devolución'})
    search = AccountSearchFilter(names=['account__contact_email',], lookup_expr='in', label=_('Buscar...'))
    account = MemberTypeFilter(label='Tipo de socia')
    paid = django_filters.BooleanFilter(field_name='paid', widget=BooleanWidget(attrs={'class': 'threestate'}))
    returned = django_filters.BooleanFilter(field_name='returned', widget=BooleanWidget(attrs={'class': 'threestate'}))

    class Meta:
        model = SocialCapital
        form = SocialCapitalFilterForm
        fields = {}


class SocialCapitalListView(PermissionRequiredMixin, FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'accounts.mespermission_can_view_social_capital'
    queryset = SocialCapital.objects.all()
    objects_url_name = 'social_capital_detail'
    template_name = 'social_capital/list.html'
    ajax_template_name = 'social_capital/query.html'
    filterset_class = SocialCapitalFilter
    paginate_by = 15


class SocialCapitalDetailView(PermissionRequiredMixin, UpdateView):
    permission_required = 'accounts.mespermission_can_view_social_capital'
    template_name = 'social_capital/detail.html'
    queryset = SocialCapital.objects.all()
    form_class = SocialCapitalForm
    model = SocialCapital

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['payment'] = PendingPayment.objects.filter(account=self.object.account) \
            .filter(Q(is_social_capital=True) | Q(concept__icontains="capital social")).first()

        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        log.error(form.errors)
        return response

    def get_success_url(self):
        return reverse('accounts:social_capital_detail', kwargs={'pk': self.object.pk})
