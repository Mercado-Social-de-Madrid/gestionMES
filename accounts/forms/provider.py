from django import forms
from django.utils.translation import gettext as _
from localflavor.es.forms import ESIdentityCardNumberField
from localflavor.generic.forms import IBANFormField

from accounts.forms.signup import BaseSignupForm
from accounts.models import Category, Provider, SocialCapital
from core.forms.BootstrapForm import BootstrapForm
from mes.settings import MEMBER_PROV


class ProviderForm(forms.ModelForm, BootstrapForm):

    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(), required=False)
    signup_ref = forms.CharField(required=False, max_length=150, widget=forms.HiddenInput())
    # cif = ESIdentityCardNumberField(label=_('NIF/CIF'))
    iban_code = IBANFormField(label=_('Cuenta bancaria (IBAN)'), required=False, widget=forms.TextInput(
        attrs={'class':'iban-code', 'placeholder':'ES0000000000000000000000'}))

    social_capital_amount = forms.FloatField(required=False, widget=forms.NumberInput(attrs={'min':0}), label='Capital social')

    required_fields = ['name', 'business_name',]

    class Meta:
        model = Provider
        exclude = ['group', 'status', 'member_type', 'cr_member', 'registration_date', 'cyclos_user',
                   'last_updated', 'collabs', 'social_capital', 'report_filename']

        widgets = {
            'contact_person': forms.TextInput(),
            'address': forms.Textarea(attrs={'rows': 3}),
            'public_address': forms.Textarea(attrs={'rows': 3}),
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'latitude': forms.NumberInput(attrs={'readonly': False}),
            'longitude': forms.NumberInput(attrs={'readonly': False}),
            'networking': forms.Textarea(attrs={'rows': 4}),
            'num_workers_male_partners':forms.NumberInput(attrs={'min':0}),
            'num_workers_female_partners':forms.NumberInput(attrs={'min':0}),
            'num_workers_male_non_partners':forms.NumberInput(attrs={'min':0}),
            'num_workers_female_non_partners':forms.NumberInput(attrs={'min':0}),
            'aprox_income': forms.NumberInput(attrs={'min': 0}),
            'num_workers': forms.NumberInput(attrs={'min': 1}),
        }

        help_texts = {
            'aprox_income': _('Expresado en miles de €')
        }

    # Overriding __init__ here allows us to provide initial data for categories
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['categories'] = [t.pk for t in kwargs['instance'].categories.all()]
            if kwargs['instance'].social_capital:
                initial['social_capital_amount'] = kwargs['instance'].social_capital.amount

        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):

        is_new = self.instance.pk is None
        instance = forms.ModelForm.save(self, False)
        instance.member_type = MEMBER_PROV

        if is_new:
            from payments.models import FeeRange
            instance.social_capital = SocialCapital.objects.create(amount=FeeRange.DEFAULT_PROVIDER_SOCIAL_CAPITAL)
            instance.social_capital.save()
        else:
            instance.social_capital.amount = self.cleaned_data['social_capital_amount']
            instance.social_capital.save()

        if not instance.public_address or instance.public_address == '':
            instance.public_address = instance.address

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the permissions to the group
           instance.categories.clear()
           instance.categories.add(*self.cleaned_data['categories'])
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance


class ProviderSignupForm(BaseSignupForm, ProviderForm):
    check_conditions = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class':'custom-control-input'}))

    required_fields = ['name', 'business_name', 'pay_by_debit', 'iban_code']
