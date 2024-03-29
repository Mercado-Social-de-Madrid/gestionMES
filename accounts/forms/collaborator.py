from django import forms
from django.utils.translation import gettext as _
from localflavor.es.forms import ESIdentityCardNumberField
from localflavor.generic.forms import IBANFormField

from accounts.models import Colaborator
from core.forms.BootstrapForm import BootstrapForm
from mes.settings import MEMBER_COLAB


class CollaboratorForm(forms.ModelForm, BootstrapForm):

    cif = ESIdentityCardNumberField(label=_('NIF/CIF'))
    iban_code = IBANFormField(label=_('Cuenta bancaria (IBAN)'), required=False, widget=forms.TextInput(
        attrs={'class': 'iban-code', 'placeholder': 'ES0000000000000000000000'}))


    class Meta:
        model = Colaborator
        exclude = ['group', 'status', 'member_type', 'cr_member', 'registration_date', 'cyclos_user',
                   'bonus_percent_entity', 'bonus_percent_general', 'max_percent_payment', 'collabs', 'member_id']

        widgets = {
            'contact_person': forms.TextInput(),
            'address': forms.Textarea(attrs={'rows': 3}),
            'public_address': forms.Textarea(attrs={'rows': 3}),
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'latitude': forms.NumberInput(attrs={'readonly': False}),
            'longitude': forms.NumberInput(attrs={'readonly': False}),
            'networking': forms.Textarea(attrs={'rows': 4}),
            'num_workers_male_partners': forms.NumberInput(attrs={'min': 0}),
            'num_workers_female_partners': forms.NumberInput(attrs={'min': 0}),
            'num_workers_male_non_partners': forms.NumberInput(attrs={'min': 0}),
            'num_workers_female_non_partners': forms.NumberInput(attrs={'min': 0}),
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

    def save(self, commit=True):

        instance = super().save(False)
        instance.member_type = MEMBER_COLAB

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

