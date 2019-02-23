from localflavor.es.forms import ESIdentityCardNumberField
from localflavor.generic.forms import IBANFormField
from django import forms
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext as _

from accounts.models import Category, Provider
from core.forms.BootstrapForm import BootstrapForm
from management.models import Comission
from mes.settings import MEMBER_PROV


class ProviderForm(forms.ModelForm, BootstrapForm):

    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(), required=False)
    signup_ref = forms.CharField(required=False, max_length=150, widget=forms.HiddenInput())
    check_conditions = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={'class':'custom-control-input'}))
    cif = ESIdentityCardNumberField(label=_('NIF/CIF'))
    iban_code = IBANFormField(label=_('Cuenta bancaria (IBAN)'), required=False, widget=forms.TextInput(
        attrs={'class':'iban-code', 'placeholder':'ES0000000000000000000000'}))

    class Meta:
        model = Provider
        exclude = ['group', 'status', 'member_type', 'cr_member', 'registration_date']
        widgets = {
            'contact_person': forms.TextInput(),
            'address': forms.Textarea(attrs={'rows': 3}),
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'latitude': forms.NumberInput(attrs={'readonly': True}),
            'longitude': forms.NumberInput(attrs={'readonly': True}),
            'networking': forms.Textarea(attrs={'rows': 4}),
            'num_workers_male_partners':forms.NumberInput(attrs={'min':0}),
            'num_workers_female_partners':forms.NumberInput(attrs={'min':0}),
            'num_workers_male_non_partners':forms.NumberInput(attrs={'min':0}),
            'num_workers_female_non_partners':forms.NumberInput(attrs={'min':0}),

        }

    # Overriding __init__ here allows us to provide initial data for permissions
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['categories'] = [t.pk for t in kwargs['instance'].categories.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'toppings' field
    def save(self, commit=True):

        is_new = self.instance.pk is None
        instance = forms.ModelForm.save(self, False)
        instance.member_type = MEMBER_PROV

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