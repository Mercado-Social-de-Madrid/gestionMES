# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.forms.category import CategoryForm
from accounts.models import Category
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin


class CategoryListView(PermissionRequiredMixin, FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'accounts.mespermission_can_manage_categories'
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