from django import forms
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext as _

from accounts.models import Category, Provider, Consumer
from core.forms.BootstrapForm import BootstrapForm
from management.models import Comission
from mes.settings import MEMBER_CONSUMER


class ConsumerForm(forms.ModelForm, BootstrapForm):

    signup_ref = forms.CharField(required=False, max_length=150, widget=forms.HiddenInput())

    class Meta:
        model = Consumer
        exclude = ['group', 'status', 'legal_form', 'member_type', 'cr_member', 'registration_date']
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