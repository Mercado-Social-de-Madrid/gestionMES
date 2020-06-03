# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.http import Http404
from django.urls import reverse
from django.utils.translation import gettext as _

from accounts.models import SignupProcess


class SignupFormMixin(object):

    def get_form_kwargs(self):
        kw = super(SignupFormMixin, self).get_form_kwargs()
        kw['from_app'] = self.request.GET.get('from_app', False)
        return kw


class SignupUpdateMixin(object):
    template_name = 'provider/edit.html'

    def getSignup(self):
        uuid = self.kwargs.get('uuid')
        process = SignupProcess.objects.filter(uuid=uuid).first()
        if not process:
            raise Http404("No se encontró el proceso")
        else:
            return process

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(self.request, _('Proceso de acogida actualizado correctamente.'))
            return reverse('accounts:signup_detail', kwargs={'pk': self.getSignup().pk})
        else:
            return reverse('accounts:signup_success')

    def form_valid(self, form):
        response = super().form_valid(form)
        process = self.getSignup()
        process.form_filled(self.object, form)
        return response

    def get_initial(self):
        process = self.getSignup()
        initial = super().get_initial()
        initial['check_privacy_policy'] = True
        initial['check_conditions'] = True
        initial['from_app'] = process.from_app
        initial['newsletter_check'] = process.newsletter_check
        initial['reference'] = process.reference
        return initial

    def get_object(self, queryset=None):
        process = self.getSignup()
        if process != None:
            account = process.account
            if account:
                account.process = process
            return account