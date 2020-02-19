from django import forms

from core.forms.BootstrapForm import BootstrapForm
from payments.models import BankBICCode


class BankForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = BankBICCode
        exclude = []

