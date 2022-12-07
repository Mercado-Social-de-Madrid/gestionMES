# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator

import django_filters
from django import db
from django.db.models import Q

from simple_bpm.models import CurrentProcess, Process, ProcessStep


class WorkflowFilter(django_filters.ChoiceFilter):

    steps = None
    filter_cancelled = False
    filter_completed = False

    def __init__(self,process_names=None, filter_cancelled=False, filter_completed=False, *args,**kwargs):

        choices = list()

        try:
            if process_names:
                processes = CurrentProcess.objects.filter(shortname__in=process_names).values_list('process', flat=True)
            else:
                processes = Process.objects.all().values_list('pk', flat=True)
            self.steps = ProcessStep.objects.filter(process__in=processes)
            choices = list(self.steps.values_list('pk', 'title'))
        except db.utils.ProgrammingError as e:
            print("Pending migrations for WorkflowFilter")

        if filter_cancelled:
            self.filter_cancelled = filter_cancelled
            choices.append(tuple(['cancelled', 'Cancelado']))

        if filter_completed:
            self.filter_completed = filter_completed
            choices.append(tuple(['completed', 'Completado']))

        django_filters.ChoiceFilter.__init__(self, choices=choices, *args,**kwargs)

    def filter(self, qs, value):

        if value == 'cancelled':
            return qs.filter(cancelled=True)

        if value == 'completed':
            return qs.filter(workflow__completed=True)

        if value not in (None,''):
            qs = qs.filter(workflow__current_state=value)

        if self.filter_cancelled:
            qs = qs.filter(cancelled=False)

        # if self.filter_completed:
        #     qs = qs.filter(workflow__completed=False)

        return qs
