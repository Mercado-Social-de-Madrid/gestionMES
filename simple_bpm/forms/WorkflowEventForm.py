from django import forms
from django.forms import widgets

from core.forms.BootstrapForm import BootstrapForm
from simple_bpm.models import ProcessWorkflowEvent


class WorkflowEventForm(forms.ModelForm, BootstrapForm):

    redirect_to = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = ProcessWorkflowEvent
        fields = ['comment', 'workflow']
        fields_required = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'workflow': forms.HiddenInput()
        }


