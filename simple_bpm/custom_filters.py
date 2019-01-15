# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator

import django_filters
from django.db.models import Q

from simple_bpm.models import CurrentProcess, Process, ProcessStep


class WorkflowFilter(django_filters.ChoiceFilter):

    steps = None

    def __init__(self,process_names=None,*args,**kwargs):

        if process_names:
            processes = CurrentProcess.objects.filter(shortname__in=process_names).values_list('process', flat=True)
        else:
            processes = Process.objects.all().values_list('pk', flat=True)
        self.steps = ProcessStep.objects.filter(process__in=processes)
        choices = self.steps.values_list('pk', 'title')
        django_filters.ChoiceFilter.__init__(self, choices=choices, *args,**kwargs)

    def filter(self,qs,value):
        print value
        if value not in (None,''):
            return qs.filter(workflow__current_state=value)

        return qs