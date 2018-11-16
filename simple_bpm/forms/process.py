# coding=utf-8
from django import forms
from django.forms import widgets

from core.forms.BootstrapForm import BootstrapForm
from simple_bpm.models import Process, ProcessStep
from django.utils.translation import gettext as _

class StepForm(forms.ModelForm, BootstrapForm):

    checklist_tasks = forms.CharField(label="Checklist", required=False, widget=widgets.HiddenInput)
    order = forms.IntegerField(widget=widgets.HiddenInput(attrs={'class':'auto-fill-order-input'}))
    title = forms.CharField(label=_('Título'), widget=widgets.TextInput(attrs={'class': 'autoupdate-text mt-2'}))
    fa_icon = forms.CharField(label=_('Icono'), required=False, widget=widgets.TextInput(attrs={'class':'fa-selector autoupdate-icon'}), initial='fas fa-wrench')

    class Meta:
        model = ProcessStep
        fields = ['order', 'title', 'description', 'fa_icon', 'checklist_tasks', 'color']
        fields_required = ['title', 'order']
        widgets = {
            'color': forms.TextInput(attrs={'class': 'color-widget'}),
        }

class ProcessForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Process
        fields = ['title', 'member_type']


def getStepsFormset(initial=True):
    return forms.formset_factory(StepForm, min_num=1, extra=0, validate_min=True )
