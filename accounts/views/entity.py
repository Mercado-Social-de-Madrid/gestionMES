# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.custom_filters import CollaborationFilter
from accounts.forms.collaborator import CollaboratorForm
from accounts.forms.entity_collab import getCollabsFormset, EditCollabForm
from accounts.mixins.feecomments import FeeCommentsMixin
from accounts.models import Category, ACTIVE, Colaborator, Entity
from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.FormsetView import FormsetView
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.TabbedViewMixin import TabbedViewMixin
from payments.models import PendingPayment
from social_balance.models import EntitySocialBalance, SocialBalanceBadge


class EntityFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class EntityFilter(django_filters.FilterSet):

    collab = CollaborationFilter(label=_('Modo de colaboración'))
    search = SearchFilter(names=['address', 'cif', 'name', 'business_name', 'contact_email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['name', 'start_year', 'registration_date'], field_labels={'name':'Nombre', 'start_year':'Año de inicio', 'registration_date':'Fecha de alta'})

    class Meta:
        model = Colaborator
        form = EntityFilterForm
        fields = { 'status':['exact'], }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.initial['status'] = ACTIVE

class EntitiesListView(FilterMixin, FilterView, ExportAsCSVMixin, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = Entity
    queryset = Entity.objects.filter(collabs__isnull=False)
    objects_url_name = 'entity_detail'
    template_name = 'entity/list.html'
    ajax_template_name = 'entity/query.html'
    filterset_class = EntityFilter
    paginate_by = 15

    csv_filename = 'proveedoras'
    available_fields = ['cif', 'name', 'business_name', 'public_address', 'address',  'contact_email', 'contact_phone', 'contact_person', 'territory',
                        'description', 'short_description', 'registered_in_app', 'current_fee', 'has_logo',
                        'postalcode', 'city', 'address', 'province', 'iban_code', 'registration_date', 'is_physical_store',
                        'start_year', 'facebook_link', 'webpage_link', 'twitter_link', 'instagram_link',
                        'telegram_link', ]
    field_labels = {'registered_in_app': 'Registrada en la app', 'current_fee': 'Cuota anual', 'has_logo':'Tiene logo'}


class CreateEntity(CreateView, FormsetView):

    form_class = CollaboratorForm
    model = Colaborator
    template_name = 'entity/create.html'

    def get_named_formsets(self):
        return {
            'collabs': getCollabsFormset(initial=True)
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def formset_collabs_valid(self, collabs, entity):
        for collab in collabs:
            collaboration = collab.save(commit=False)
            collaboration.entity = entity
            collaboration.save()


    def get_success_url(self):
        messages.success(self.request, _('Entidad añadida correctamente.'))
        return reverse('accounts:entity_list')



class EntityDetailView(TabbedViewMixin, FeeCommentsMixin, UpdateView):
    template_name = 'entity/detail.html'
    default_tab = 'details'
    available_tabs = ['details', 'payments',]
    form_class = CollaboratorForm
    model = Colaborator

    def get_success_url(self):
        return reverse('accounts:entity_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['payments'] = PendingPayment.objects.filter(account=self.object)
        context['signup'] = self.object.signup_process.first()
        context['social_balances'] = EntitySocialBalance.objects.filter(entity=self.object).order_by('year')
        context['current_balance'] = EntitySocialBalance.objects.filter(entity=self.object, year=settings.CURRENT_BALANCE_YEAR).first()
        context['current_badge'] =  SocialBalanceBadge.objects.filter(year=settings.CURRENT_BALANCE_YEAR).first()
        context['profile_tab'] = True

        collabs = self.object.get_active_collaborations()
        if (len(collabs) > 0):
            context['collabs'] = []
            for collab in collabs:
                context['collabs'].append(EditCollabForm(instance=collab))

        return context
