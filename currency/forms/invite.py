# coding=utf-8
from datetime import datetime
import dateutil
from django import forms
from django.contrib.auth.models import Permission, Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from accounts.models import Category, Provider
from core.forms.BootstrapForm import BootstrapForm
from currency.models import GuestInvitation, INVITE_DURATION_MONTHS
from management.models import Comission
from mes.settings import MEMBER_PROV


class GuestInviteForm(forms.ModelForm, BootstrapForm):

    invite_token = forms.CharField(required=False, max_length=150, widget=forms.HiddenInput())

    class Meta:
        model = Provider
        exclude = ['active', 'expiration_date', 'registration_date', 'invited_by']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


    def clean(self):
        data = self.cleaned_data

        invite_token = data.get('invite_token', '')
        if not GuestInvitation.objects.is_valid_token(invite_token):
            raise ValidationError(_('Token de invitación no válido'))

        return data

    def save(self, commit=True):

        invited_by = GuestInvitation.objects.filter(self.cleaned_data.get('invite_token')).first().invited_by
        instance = forms.ModelForm.save(self, False)
        instance.invited_by = invited_by
        instance.registration_date = datetime.now()
        instance.expiration_date = datetime.now() + dateutil.relativedelta.relativedelta(months=INVITE_DURATION_MONTHS)

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance