from django import forms
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext as _

from accounts.models import Category, Provider, Consumer, SignupProcess
from core.forms.BootstrapForm import BootstrapForm
from management.models import Comission
from mes.settings import MEMBER_CONSUMER


class SignupProcessForm(forms.ModelForm, BootstrapForm):

    required_fields = ['member_type', 'name']

    class Meta:
        model = SignupProcess
        exclude = ['workflow', 'account', 'uuid']

