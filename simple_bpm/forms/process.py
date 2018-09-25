from django import forms
from django.forms import formset_factory

from simple_bpm.models import Process


class ProcessForm(forms.ModelForm):

    class Meta:
        model = Process
        fields = ['order', 'image', 'title']
