from django import forms

text_widget_class = 'form-control'
select_widget_class = 'custom-select'

class BootstrapModelForm(forms.Form):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            widget_class = select_widget_class if field.widget.input_type == 'select' else text_widget_class

            if 'class' in field.widget.attrs:
                if widget_class not in field.widget.attrs['class']:
                   field.widget.attrs['class'] += ' ' + widget_class
            else:
                field.widget.attrs['class'] = widget_class

            if not 'placeholder' in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label
