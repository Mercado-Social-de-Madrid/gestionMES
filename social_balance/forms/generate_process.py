from django import forms
from django.utils.translation import gettext as _

from core.forms.BootstrapForm import BootstrapForm
from social_balance.models import BALANCE_TYPES

DELIMITER_CHOICES = ( (',',', (coma)'), (';','; (punto y coma)'), ('|','| (barra vertical)') )

class GenerateProcessForm(BootstrapForm):

    year = forms.IntegerField(min_value=0, required=True, label=_('Año'), help_text=_('Año'))
    balance_type = forms.ChoiceField(choices=BALANCE_TYPES, label=_('Tipo de balance'))

    required_fields = ['balance_type', 'year']
