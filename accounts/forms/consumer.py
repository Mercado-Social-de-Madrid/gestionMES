from django import forms
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext as _
from localflavor.es.forms import ESIdentityCardNumberField
from localflavor.generic.forms import IBANFormField

from accounts.forms.signup import BaseSignupForm
from accounts.models import Category, Provider, Consumer
from core.forms.BootstrapForm import BootstrapForm
from management.models import Comission
from mes.settings import MEMBER_CONSUMER


class ConsumerForm(forms.ModelForm, BootstrapForm):

    signup_ref = forms.CharField(required=False, max_length=150, widget=forms.HiddenInput())
    cif = ESIdentityCardNumberField(label=_('NIF/CIF'))
    iban_code = IBANFormField(label=_('Cuenta bancaria (IBAN)'), required=True, widget=forms.TextInput(
        attrs={'class': 'iban-code', 'placeholder': 'ES0000000000000000000000'}))


    required_fields = ['first_name', 'last_name', 'pay_by_debit']

    class Meta:
        model = Consumer
        exclude = ['group', 'status', 'legal_form', 'member_type', 'cr_member', 'registration_date', 'cyclos_user']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):

        instance = forms.ModelForm.save(self, False)
        instance.member_type = MEMBER_CONSUMER

        # Do we need to save all changes now?
        if commit:
            instance.save()

        return instance

class ConsumerSignupForm(BaseSignupForm, ConsumerForm):
    pass
