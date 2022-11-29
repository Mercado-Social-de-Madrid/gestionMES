# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.utils.translation import gettext as _
from django.db import models

from core.models import User
from mes import settings


class Process(models.Model):

    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    member_type = models.CharField(null=True, blank=True,max_length=30, choices=settings.MEMBER_TYPES, verbose_name=_('Tipo de socia'))

    class Meta:
        verbose_name = _('Proceso')
        verbose_name_plural = _('Procesos')
        permissions = (
            ("mespermission_can_manage_processes", _("Puede gestionar los procesos")),
        )

    def __str__(self):
        return self.title or 'Process'


class ProcessStep(models.Model):

    process = models.ForeignKey(Process, null=False, on_delete=models.CASCADE, verbose_name=_('Proceso'), related_name='steps')
    order = models.IntegerField(default=0, verbose_name=('Orden'))
    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))
    fa_icon = models.CharField(null=True, blank=True, verbose_name=_('Icono del paso'), max_length=50)
    color = models.CharField(max_length=20, blank=True, default="#653776")

    class Meta:
        verbose_name = _('Paso de un proceso')
        verbose_name_plural = _('Pasos de un proceso')
        ordering = ['order']

    def __str__(self):
        return "{} - {}".format(self.process.title, self.title)

    def is_named_step(self, shortname):
        return CurrentProcessStep.objects.filter(process_step=self, shortname=shortname).exists()


class ProcessStepTask(models.Model):
    process_step = models.ForeignKey(ProcessStep, null=False, on_delete=models.CASCADE, verbose_name=_('Tarea de un proceso'),
                                related_name='checklist')
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))

    class Meta:
        verbose_name = _('Tarea de un proceso')
        verbose_name_plural = _('Tareas de un proceso')


# Class to define the current process established for each of the bussiness processes defined
class CurrentProcess(models.Model):

    shortname = models.CharField(primary_key=True, unique=True, verbose_name=_('Nombre corto'), max_length=50)
    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)
    process = models.ForeignKey(Process, null=True, verbose_name=_('Proceso asociado'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Proceso asignado')
        verbose_name_plural = _('Procesos asignados')
        permissions = (
            ("mespermission_can_manage_current_process", _("Puede gestionar los procesos asociados a cada tarea")),
        )

# Class to define the concrete step inside a process
class CurrentProcessStep(models.Model):
    process = models.ForeignKey(Process, verbose_name=_('Proceso asociado'), on_delete=models.CASCADE)
    process_step = models.ForeignKey(ProcessStep, null=True, on_delete=models.CASCADE,
                                     verbose_name=_('Paso del proceso'))
    shortname = models.CharField(primary_key=True, unique=False, verbose_name=_('Nombre corto'), max_length=50)

    class Meta:
        verbose_name = _('Paso asignado del proceso')
        verbose_name_plural = _('Paso asignado del proceso')


class ProcessWorkflow(models.Model):
    process = models.ForeignKey(Process, verbose_name=_('Proceso que sigue'), on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha de inicio'))
    current_state = models.ForeignKey(ProcessStep, null=True, verbose_name=_('Paso actual'), on_delete=models.CASCADE)
    completed = models.BooleanField(default=False, verbose_name=_('Completado'))

    class Meta:
        verbose_name = _('Workflow de Proceso')
        verbose_name_plural = _('Workflows de proceso')

    def get_first_step(self):
        return ProcessStep.objects.filter(process=self.process).order_by('order').first()

    def get_last_step(self):
        return ProcessStep.objects.filter(process=self.process).order_by('order').last()

    def get_step(self, order):
        return ProcessStep.objects.filter(process=self.process, order=order).first()

    def get_previous_step(self):
        order = self.current_state.order if self.current_state != None else 0
        return ProcessStep.objects.filter(process=self.process, order__lt=order).order_by('-order').first()

    def get_next_step(self):
        order = self.current_state.order if self.current_state != None else 0
        return ProcessStep.objects.filter(process=self.process, order__gt=order).order_by('order').first()

    def is_first_step(self):
        return self.current_state != None and self.get_first_step() == self.current_state

    def add_comment(self, user, comment, timestamp=None):

        event = ProcessWorkflowEvent()
        event.workflow = self
        event.step = None
        event.completed_by = user
        event.comment = comment
        if timestamp:
            event.timestamp = timestamp
        event.save()

    def revert_current_step(self):
        current_step = self.current_state
        previous_step = self.get_previous_step()

        if previous_step:
            # We delete the current step event in the history
            ProcessWorkflowEvent.objects.filter(workflow=self, step__in=[current_step,previous_step]).delete()
            self.current_state = previous_step
            self.completed = False
            self.save()

    def complete_current_step(self, user=None):

        current_step = self.current_state
        next_step = self.get_next_step()

        if next_step is None:
            # We are in the last step!
            self.current_state = None
            self.completed = True
            self.save()
        else:
            self.current_state = next_step
            self.save()

        event = ProcessWorkflowEvent()
        event.workflow = self
        event.step = current_step
        event.completed_by = user
        event.save()

        if self.completed:
            # we create also the special completion event
            self.add_special_event('completed', user)


    def add_special_event(self, special_type, user=None):
        event = ProcessWorkflowEvent()
        event.workflow = self
        event.completed_by = user
        event.special = True
        event.special_type = special_type
        event.save()


SPECIAL_EVENTS = (
    ('completed', 'Completado'),
    ('cancelled', 'Cancelado'),
    ('restarted', 'Reiniciado'),
)

class ProcessWorkflowEvent(models.Model):
    workflow = models.ForeignKey(ProcessWorkflow, verbose_name=_('Evento de un proceso'), related_name='history_events', on_delete=models.CASCADE)
    step = models.ForeignKey(ProcessStep, null=True, verbose_name=_('Paso del proceso'), on_delete=models.CASCADE)
    completed_by = models.ForeignKey(User, null=True, verbose_name=_('Usuario'), on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(verbose_name=_('Fecha'))
    comment = models.TextField(blank=True, null=True, verbose_name=_('Comentario'))
    special = models.BooleanField(default=False, verbose_name=_('Evento especial'))
    special_type = models.CharField(null=True, choices=SPECIAL_EVENTS, max_length=15, verbose_name=_('Tipo de evento especial'))

    class Meta:
        verbose_name = _('Evento de Proceso')
        verbose_name_plural = _('Eventos de proceso')
        ordering = ['-timestamp']

    def save(self, *args, **kwargs):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now()
        super().save(*args, **kwargs)



class ProcessWorkflowTask(models.Model):
    workflow = models.ForeignKey(ProcessWorkflow, verbose_name=_('Evento de un proceso'), related_name='completed_checklist', on_delete=models.CASCADE)
    task = models.ForeignKey(ProcessStepTask, null=True, verbose_name=_('Tarea completada'), on_delete=models.CASCADE)
    completed_by = models.ForeignKey(User, verbose_name=_('Usuario'), null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha'))

    class Meta:
        verbose_name = _('Tarea completadas del proceso')
        verbose_name_plural = _('Tareas completadas del proceso')

