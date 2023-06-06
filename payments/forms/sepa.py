from django import forms
from django.conf import settings

from core.forms.BootstrapForm import BootstrapForm
from payments.models import SepaPaymentsBatch, PendingPayment, SepaBatchResult


class SepaBatchForm(forms.ModelForm, BootstrapForm):
    payments = forms.ModelMultipleChoiceField(queryset=PendingPayment.objects.filter(), required=False, )
    payments_order = forms.CharField(widget=forms.HiddenInput())
    required_fields = []

    class Meta:
        model = SepaPaymentsBatch
        exclude = ['sepa_file', 'amount', 'attempt']

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)

        self.save_m2m = self.save_many2many

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

            total_amount = 0
            for payment in instance.payments.all():
                total_amount += payment.amount
            instance.amount = total_amount
            instance.save()

            instance.preprocess_batch()
            instance.generate_batch()

        return instance

    def save_many2many(self):
        instance = self.instance
        non_updated_batch_payments = set(instance.batch_payments.all())
        paymentsOrder = self.cleaned_data['payments_order']
        paymentsOrder = paymentsOrder.split(settings.INLINE_INPUT_SEPARATOR)
        for payment in self.cleaned_data['payments'].all():
            order = paymentsOrder.index(str(payment.pk))
            sepa_batch_result, created = SepaBatchResult.objects.update_or_create(
                payment=payment,
                batch=instance,
                defaults={
                    'order': order
                }
            )
            non_updated_batch_payments -= {sepa_batch_result}  # Ignore batch_payment if updated/created
        for batch_payment in non_updated_batch_payments:
            batch_payment.delete()
