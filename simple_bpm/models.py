# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import gettext as _
from django.db import models

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


class ProcessStep(models.Model):

    process = models.ForeignKey(Process, null=False, on_delete=models.CASCADE, verbose_name=_('Proceso'), related_name='steps')
    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))
    fa_icon = models.CharField(null=True, blank=True, verbose_name=_('Icono del paso'), max_length=50)

    class Meta:
        verbose_name = _('Paso de un proceso')
        verbose_name_plural = _('Pasos de un proceso')


class ProcessStepTask(models.Model):
    process_step = models.ForeignKey(ProcessStep, null=False, on_delete=models.CASCADE, verbose_name=_('Tarea de un proceso'),
                                related_name='checklist')
    description = models.TextField(null=True, blank=True, verbose_name=_('Descripción'))

    class Meta:
        verbose_name = _('Tarea de un proceso')
        verbose_name_plural = _('Tareas de un proceso')


# Class to define the current process established for each of the bussiness processes defined
class CurrentProcess(models.Model):

    title = models.CharField(null=True, blank=True, verbose_name=_('Título'), max_length=250)

    class Meta:
        verbose_name = _('Proceso asignado')
        verbose_name_plural = _('Procesos asignados')
        permissions = (
            ("mespermission_can_manage_current_process", _("Puede gestionar los procesos asociados a cada tarea")),
        )
