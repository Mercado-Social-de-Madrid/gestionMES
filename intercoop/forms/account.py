from django import forms

from core.forms.BootstrapForm import BootstrapForm
from intercoop.models import IntercoopAccount


class IntercoopAccountForm(forms.ModelForm, BootstrapForm):



    class Meta:
        model = IntercoopAccount
        exclude = []

    check_privacy_policy = forms.BooleanField(required=True,
                                              widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))
    check_share_data = forms.BooleanField(required=True,
                                              widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))