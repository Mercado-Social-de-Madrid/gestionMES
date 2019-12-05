from django import forms


from core.forms.BootstrapForm import BootstrapForm
from intercoop.models import IntercoopEntity


class IntercoopEntityForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = IntercoopEntity
        exclude = []

