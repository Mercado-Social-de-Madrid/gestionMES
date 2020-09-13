# coding=utf-8
from django import forms

from accounts.models import Collaboration
from core.forms.BootstrapForm import BootstrapForm


class CollabForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Collaboration
        widgets = {
            'color': forms.TextInput(attrs={'class': 'color-widget'}),
        }
        exclude = []
