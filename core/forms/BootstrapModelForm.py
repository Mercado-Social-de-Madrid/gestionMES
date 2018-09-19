from django import forms

field_class = 'form-control'

class BootstrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                if field_class not in field.widget.attrs['class']:
                   field.widget.attrs['class'] += ' ' + field_class
            else:
                field.widget.attrs['class'] = field_class
