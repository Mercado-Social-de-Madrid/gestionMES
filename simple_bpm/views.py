# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView

from core.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from simple_bpm.models import Process



class ProcessesListView(ListView, AjaxTemplateResponseMixin):
    model = Process
    template_name = 'bpm/list.html'
    ajax_template_name = 'bpm/query.html'
    paginate_by = 2



def register(request):

    processes = Process.objects.all()

    return render(request, 'registration/signup.html', {'processes': processes})

