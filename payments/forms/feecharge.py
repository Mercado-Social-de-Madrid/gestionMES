# coding=utf-8
from django import forms
from core.forms.BootstrapForm import BootstrapForm
from payments.models import AccountAnnualFeeCharge


class FeeSplitForm(BootstrapForm):
    date = forms.DateField(label='Fecha', required=True)
    amount = forms.FloatField(label='Cantidad', required=True, min_value=0)
    concept = forms.CharField(label='Concepto', required=True)


class AccountFeeSplitForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = AccountAnnualFeeCharge
        fields = ['amount', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows':3})
        }


def getFeeSplitFormset(initial=True):
    return forms.formset_factory(FeeSplitForm, min_num=2, extra=0, validate_min=True )
