# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic import UpdateView, CreateView
from django_filters.views import FilterView
from filters.views import FilterMixin

from accounts.forms.category import CategoryForm
from accounts.forms.collaboration import CollabForm
from accounts.forms.entity_collab import EditCollabForm
from accounts.models import Category, Collaboration, EntityCollaboration
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin


class CollaborationListView(PermissionRequiredMixin, FilterMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'accounts.mespermission_can_manage_categories'
    queryset = Collaboration.objects.all()
    model = Collaboration
    objects_url_name = 'collab_detail'
    template_name = 'collab/list.html'
    ajax_template_name = 'collab/query.html'
    paginate_by = 15

    def get_queryset(self):
        qs = Collaboration.objects.all().annotate(total=Count('entities_collab'))
        return qs


class CollaborationCreate(CreateView):

    form_class = CollabForm
    model = Collaboration
    template_name = 'collab/create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Colaboración añadida correctamente.'))
        return response

    def get_success_url(self):
        return reverse('accounts:collab_list')


class CollaborationDetailView(UpdateView):
    template_name = 'collab/detail.html'
    form_class = CollabForm
    model = Collaboration

    def get_success_url(self):
        return reverse('accounts:collab_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Datos actualizados correctamente.'))
        return response


class EntityCollaborationUpdate(UpdateView):

    model = EntityCollaboration
    form_class = EditCollabForm

    def get_success_url(self):
        if self.redirect_url:
            return self.redirect_url
        else:
            return reverse('accounts:entity_detail', kwargs={'pk': self.object.entity.pk})

    def form_valid(self, form):
        self.redirect_url = form.cleaned_data.get('redirect_to')
        if 'delete' in self.request.POST:
            self.object.delete()
            messages.success(self.request, _('Colaboración eliminada correctamente.'))
            return HttpResponseRedirect(self.get_success_url())
        else:
            response = super().form_valid(form)
            messages.success(self.request, _('Datos actualizados correctamente.'))
            return response
