from django import forms

from core.forms.BootstrapForm import BootstrapForm
from intercoop.models import IntercoopAccount
from accounts.forms.signup import BaseSignupForm

class IntercoopAccountForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = IntercoopAccount
        exclude = []
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class IntercoopAccountSignupForm(BaseSignupForm):

    check_share_data = forms.BooleanField(required=True,
                                              widget=forms.CheckboxInput(attrs={'class': 'custom-control-input'}))

    class Meta:
        model = IntercoopAccount
        exclude = []
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
