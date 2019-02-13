# coding=utf-8
from datetime import datetime
import dateutil
from django import forms
from django.contrib.auth.models import Permission, Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from accounts.models import Category, Provider
from core.forms.BootstrapForm import BootstrapForm
from currency.models import GuestInvitation, INVITE_DURATION_MONTHS, GuestAccount
from management.models import Comission
from mes.settings import MEMBER_PROV


class GuestAccountForm(forms.ModelForm, BootstrapForm):


    class Meta:
        model = GuestAccount
        exclude = []
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
