from django import forms

from core.forms.BootstrapForm import BootstrapForm
from social_balance.models import SocialBalanceBadge


class SocialBadgeForm(forms.ModelForm, BootstrapForm):


    required_fields = ['year', 'base_img',]

    class Meta:
        model = SocialBalanceBadge
        exclude= []

        widgets = {
            'layout_json': forms.HiddenInput(),
        }