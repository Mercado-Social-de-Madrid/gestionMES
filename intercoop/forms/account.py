from django import forms

from core.forms.BootstrapForm import BootstrapForm
from intercoop.models import IntercoopAccount
from accounts.forms.signup import BaseSignupForm

class IntercoopAccountForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = IntercoopAccount
        exclude = []


class IntercoopAccountSignupForm(BaseSignupForm):

    class Meta:
        model = IntercoopAccount
        exclude = []
