from django import forms
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext as _


from core.forms.BootstrapForm import BootstrapForm
from management.models import Comission
from mes.settings import MEMBER_PROV
from payments.models import PendingPayment


class PaymentForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = PendingPayment
        exclude = ['reference', 'revised_by']
        widgets = {
            'account': forms.HiddenInput()
        }