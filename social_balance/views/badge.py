# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from accounts.models import Entity
from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from core.mixins.ListItemUrlMixin import ListItemUrlMixin
from social_balance.forms.badge import SocialBadgeForm
from social_balance.models import SocialBalanceBadge, EntitySocialBalance


class BadgesListView(PermissionRequiredMixin, ListView, ListItemUrlMixin, AjaxTemplateResponseMixin):
    permission_required = 'social_balance.mespermission_can_view_social_badges'
    queryset = SocialBalanceBadge.objects.all()
    model = SocialBalanceBadge
    objects_url_name = 'badge_detail'
    template_name = 'balance_badge/list.html'
    ajax_template_name = 'balance_badge/query.html'
    filterset_class = None
    paginate_by = 5


class NewSocialBadge(CreateView):
    form_class = SocialBadgeForm
    model = SocialBalanceBadge
    template_name = 'balance_badge/create.html'

    def get_success_url(self):
        return reverse('balance:badge_detail', kwargs={'pk': self.object.pk})


class SocialBadgeDetailView(DetailView):
    template_name = 'balance_badge/detail.html'
    queryset = SocialBalanceBadge.objects.all()
    model = SocialBalanceBadge


class SocialBadgeEditView(UpdateView):
    form_class = SocialBadgeForm
    template_name = 'balance_badge/edit.html'
    queryset = SocialBalanceBadge.objects.all()
    model = SocialBalanceBadge

    def get_success_url(self):
        return reverse('balance:badge_detail',  kwargs={'pk': self.object.pk})


class SocialBadgeRender(DetailView):
    template_name = 'balance_badge/render.html'
    queryset = SocialBalanceBadge.objects.all()
    model = SocialBalanceBadge

    def get_context_data(self, **kwargs):
        context = super(SocialBadgeRender, self).get_context_data(**kwargs)
        entity_id = self.request.GET.get('id', None)
        context['entity'] = Entity.objects.get(id=entity_id)
        context['balance'] = EntitySocialBalance.objects.get(entity=context['entity'], year=self.object.year)
        context['hide_navbar'] = True

        return context

