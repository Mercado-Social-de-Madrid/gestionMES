from django import forms

from accounts.models import SocialCapital
from core.forms.BootstrapForm import BootstrapForm


class SocialCapitalForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = SocialCapital
        exclude = []
