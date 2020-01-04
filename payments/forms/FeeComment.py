from django import forms
from django.forms import widgets

from core.forms.BootstrapForm import BootstrapForm
from payments.models import FeeComments
from simple_bpm.models import ProcessWorkflowEvent


class FeeCommentForm(forms.ModelForm, BootstrapForm):

    redirect_to = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FeeComments
        fields = ['comment', 'account']
        fields_required = ['comment']

        widgets = {
            'account': forms.HiddenInput()
        }


