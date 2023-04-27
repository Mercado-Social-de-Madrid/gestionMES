from django import forms
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext as _
from localflavor.es.forms import ESIdentityCardNumberField
from localflavor.generic.forms import IBANFormField

from accounts.forms.signup import BaseSignupForm
from accounts.models import Category, Provider, Consumer, SocialCapital
from core.forms.BootstrapForm import BootstrapForm
from management.models import Comission
from mes.settings import MEMBER_CONSUMER


class ConsumerForm(forms.ModelForm, BootstrapForm):

    signup_ref = forms.CharField(required=False, max_length=150, widget=forms.HiddenInput())
    # cif = ESIdentityCardNumberField(label=_('NIF/CIF'))
    iban_code = IBANFormField(label=_('Cuenta bancaria (IBAN)'), required=False, widget=forms.TextInput(
        attrs={'class': 'iban-code', 'placeholder': 'ES0000000000000000000000'}))

    social_capital_amount = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'min':0}), label='Capital social')

    required_fields = ['first_name', 'last_name', ]

    class Meta:
        model = Consumer
        exclude = ['group', 'status', 'legal_form', 'member_type', 'cr_member', 'registration_date', 'cyclos_user',
                   'social_capital', 'member_id']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    # Overriding __init__ here allows us to provide initial data
    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            if kwargs['instance'].social_capital:
                initial['social_capital_amount'] = kwargs['instance'].social_capital.amount

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):

        is_new = self.instance.pk is None
        instance = forms.ModelForm.save(self, False)
        instance.member_type = MEMBER_CONSUMER

        if is_new:
            from payments.models import FeeRange
            instance.social_capital = SocialCapital.objects.create(amount=FeeRange.DEFAULT_CONSUMER_SOCIAL_CAPITAL)
            instance.social_capital.save()
        else:
            instance.social_capital.amount = self.cleaned_data['social_capital_amount']
            instance.social_capital.save()

        if commit:
            instance.save()

        return instance


class ConsumerSignupForm(BaseSignupForm, ConsumerForm):

    required_fields = ['first_name', 'last_name', 'pay_by_debit', 'iban_code']
