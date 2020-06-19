# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView

from accounts.models import Provider, Consumer, Account, OPTED_OUT, Colaborator, SignupProcess
from core.forms.password import PasswordForm
from core.forms.profile import ProfileForm
from core.forms.signup import SignUpForm
from simple_bpm.models import ProcessStep


class dashboard(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['year'] = date.today().year
        return context


class accounts(TemplateView):
    template_name = 'dashboard/accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        year = date.today().year
        provider_signups = Provider.objects.filter(registration_date__year=year)
        consumer_signups = Consumer.objects.filter(registration_date__year=year)
        account_optedout = Account.objects.filter(status=OPTED_OUT, opted_out_date__year=year)

        context['provider_signups'] = provider_signups.count()
        context['consumer_signups'] = consumer_signups.count()
        context['account_optedout'] = account_optedout.count()
        context['num_accounts'] = Account.objects.active().count()
        context['num_providers'] = Provider.objects.active().count()
        context['num_consumers'] = Consumer.objects.active().count()
        context['num_special'] = Colaborator.objects.active().count()

        context['year'] = year
        context['signups'] = Account.objects.active().filter(registration_date__year=year).annotate(month=TruncMonth('registration_date')).values('month').annotate(total=Count('id')).values('month', 'total')

        return context


class signups(TemplateView):
    template_name = 'dashboard/signups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        year = date.today().year

        signups = SignupProcess.objects.pending().filter(last_update__year=year)
        signup_statuses = {}
        for signup in signups:
            if signup.workflow.current_state.pk in signup_statuses:
                signup_statuses[signup.workflow.current_state.pk]['count'] += 1
            else:
                signup_statuses[signup.workflow.current_state.pk] = {
                    'step': signup.workflow.current_state,
                    'count': 1
                }

        context['signups'] = signups
        context['closed_signups'] = SignupProcess.objects.filter(last_update__year=year, workflow__completed=True).count()
        context['cancelled_signups'] = SignupProcess.objects.filter(last_update__year=year, cancelled=True).count()
        context['signup_statuses'] = signup_statuses

        return context