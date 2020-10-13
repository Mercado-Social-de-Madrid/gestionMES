# coding=utf-8
from django import forms
from django.forms import widgets

from accounts.models import EntityCollaboration
from core.forms.BootstrapForm import BootstrapForm
from simple_bpm.models import Process, ProcessStep
from django.utils.translation import gettext as _

class EntityCollabForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = EntityCollaboration
        fields = ['collaboration', 'special_agreement', 'custom_fee', 'started', 'ended']
        fields_required = ['collaboration', 'special_agreement']

        widgets = {
            'special_agreement': forms.Textarea(attrs={'rows': 5})
        }

class EditCollabForm(forms.ModelForm, BootstrapForm):

    redirect_to = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = EntityCollaboration
        exclude = []

        widgets = {
            'entity': forms.HiddenInput(),
            'special_agreement': forms.Textarea(attrs={'rows': 4})
        }


def getCollabsFormset(initial=True):
    return forms.formset_factory(EntityCollabForm, min_num=1, extra=0, validate_min=True )
