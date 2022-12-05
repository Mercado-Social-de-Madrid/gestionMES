from django import forms

from core.forms.BootstrapForm import BootstrapForm
from social_balance.models import EntitySocialBalance


class EntityYearBalanceForm(forms.ModelForm, BootstrapForm):

    required_fields = ['year']

    class Meta:
        model = EntitySocialBalance
        exclude = ['badge_image', 'external_id', 'report_filename']

        widgets = {
            'entity': forms.HiddenInput(),
            'year': forms.HiddenInput(),
            'achievement': forms.Textarea(attrs={'rows': 3}),
            'challenge': forms.Textarea(attrs={'rows': 3}),
        }