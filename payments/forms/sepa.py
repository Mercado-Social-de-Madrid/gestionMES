from django import forms

from core.forms.BootstrapForm import BootstrapForm
from mes.settings import MEMBER_PROV
from payments.models import SepaBatch, PendingPayment


class SepaBatchForm(forms.ModelForm, BootstrapForm):
    payments = forms.ModelMultipleChoiceField(queryset=PendingPayment.objects.filter(), required=False, )

    required_fields = []

    class Meta:
        model = SepaBatch
        exclude = ['sepa_file', 'amount', 'attempt']


    def save(self, commit=True):

        instance = forms.ModelForm.save(self, False)
        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the permissions to the group
           instance.payments.clear()
           instance.payments.add(*self.cleaned_data['payments'])
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

            total_amount = 0
            for payment in instance.payments.all():
                total_amount += payment.amount
            instance.amount = total_amount
            instance.save()

            instance.generate_batch()


        return instance

