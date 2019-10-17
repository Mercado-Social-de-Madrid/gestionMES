# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView, TemplateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from core.filters.LabeledOrderingFilter import LabeledOrderingFilter
from core.filters.SearchFilter import SearchFilter
from core.forms.BootstrapForm import BootstrapForm
from core.forms.password import PasswordForm
from core.forms.profile import ProfileForm
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from core.mixins.TabbedViewMixin import TabbedViewMixin
from core.models import User
from management.forms.commission import CommissionForm
from management.forms.user import UserForm
from management.models import Comission


class UserFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'is_active', ]


class UserFilter(django_filters.FilterSet):

    search = SearchFilter(names=['username', 'first_name', 'last_name', 'email'], lookup_expr='in', label=_('Buscar...'))
    o = LabeledOrderingFilter(fields=['username', 'last_login', 'date_joined'])

    class Meta:
        model = User
        form = UserFilterForm
        fields = { 'is_active':['exact'], }


class UsersListView(FilterMixin, ExportAsCSVMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = User
    queryset = User.objects.all()
    objects_url_name = 'user_detail'
    template_name = 'user/list.html'
    ajax_template_name = 'user/query.html'
    filterset_class = UserFilter
    paginate_by = 5

    csv_filename = 'usuarias'
    available_fields = ['username', 'email', 'is_active', 'date_joined', 'display_name', 'last_login']
    field_labels = {'display_name': 'Nombre completo'}


class UserDetailView(UpdateView):
    template_name = 'user/detail.html'
    password_form = PasswordForm
    form_class = ProfileForm
    profile_form = ProfileForm
    success_url = '/dashboard'
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = self.get_object()
        if 'password_form' not in context:
            context['password_form'] = self.password_form(user=user)
        if 'profile_form' not in context:
            context['profile_form'] = self.profile_form(instance=user)
        if 'form_focus' not in context:
            context['form_focus'] = 'profile_form'

        context['profile_tab'] = True
        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def get_simple_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'profile_form' in request.POST:
            form_name = 'profile_form'
            form = self.profile_form(**self.get_form_kwargs())
        else:
            form_name = 'password_form'
            form = self.password_form(user=self.object, **self.get_simple_kwargs())

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{'form_focus': form_name, form_name: form})


class UsersCreate(CreateView):

    form_class = UserForm
    model = User
    template_name = 'user/create.html'

    def form_valid(self, form):
        response = super(UsersCreate, self).form_valid(form)
        self.object.groups.add(form.cleaned_data['group'])
        messages.success(self.request, _('Usuario añadido correctamente.'))
        return response

    def get_success_url(self):
        return reverse('management:users_list')


class ComissionsListView(FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    queryset = Comission.objects.all()
    objects_url_name = 'commission_detail'
    model = Comission
    template_name = 'commission/list.html'
    ajax_template_name = 'commission/query.html'
    paginate_by = 10


class CommissionCreate(CreateView):

    form_class = CommissionForm
    model = Comission
    template_name = 'commission/create.html'

    def form_valid(self, form):
        response = super(CommissionCreate, self).form_valid(form)
        messages.success(self.request, _('Comisión añadida correctamente.'))
        return response

    def get_success_url(self):
        return reverse('management:commission_list')


class CommissionDetailView(TabbedViewMixin, UpdateView):
    template_name = 'commission/detail.html'
    default_tab = 'permissions'
    available_tabs = ['permissions', 'members']
    form_class = CommissionForm
    model = Comission

    def get_success_url(self):
        return reverse('management:commission_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super(CommissionDetailView, self).form_valid(form)
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return response


class CommissionMembers(TemplateView):

    template_name = 'commission/members.html'

    def dispatch(self, request, *args, **kwargs):
        self.commission = kwargs.get('pk', None)
        return super(CommissionMembers, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CommissionMembers, self).get_context_data(**kwargs)
        context['commission'] = get_object_or_404(Comission, pk=self.commission)
        context['all_users'] = User.objects.filter(is_active=True).exclude(groups__comission=context['commission'])
        return context

    def post(self, post, *args, **kwargs):
        commission = get_object_or_404(Comission, pk=self.commission)
        members = self.request.POST.getlist('members[]', default='')

        users = User.objects.filter(pk__in=members)
        commission.group.user_set.clear()
        commission.group.user_set.add(*users)

        return HttpResponse(200)