from django import forms

from core.forms.BootstrapForm import BootstrapForm


class BaseSignupForm(forms.ModelForm, BootstrapForm):
    check_privacy_policy = forms.BooleanField(required=True,
                                              widget=forms.CheckboxInput(attrs={'class':'custom-control-input'}))

