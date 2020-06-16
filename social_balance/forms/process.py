from django import forms

from core.forms.BootstrapForm import BootstrapForm
from social_balance.models import BalanceProcess


class ProcessSponsorForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = BalanceProcess
        fields = ['sponsor', 'balance_type']

