import codecs
import csv
from itertools import islice

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from core.forms.BootstrapForm import BootstrapForm
from django.utils.translation import gettext as _

from helpers.csv import csv_missing_fields


DELIMITER_CHOICES = ( (',',', (coma)'), (';','; (punto y coma)'), ('|','| (barra vertical)') )

class ImportSocialBalanceForm(BootstrapForm):

    year = forms.IntegerField(min_value=0, required=True, label=_('Año'), help_text=_('Año al que corresponden los datos de balance social (por ejemplo, en la campaña de 2020 los datos son los de 2019)'))
    csv_file = forms.FileField(required=True, label=_('Fichero CSV'),
                               validators=[FileExtensionValidator(allowed_extensions=['csv', 'data', 'txt'])])
    delimiter = forms.ChoiceField(choices=DELIMITER_CHOICES, label=_('Delimitador CSV'))

    required_fields = ['cif', 'exenta', 'realizado', 'publico', 'logro', 'reto']

    # Check that the CSV file contains all the required fields
    def clean(self):
        super().clean()
        file = self.cleaned_data['csv_file']
        delimiter = self.cleaned_data['delimiter']

        missing_headers = csv_missing_fields(file, self.required_fields, delimiter)

        if missing_headers:
            raise ValidationError(
                _('Faltan columnas obligatorias en la cabecera del CSV: %(missing_headers)s'),
                params = {'missing_headers': ', '.join(missing_headers)}
            )

        return self.cleaned_data