from django import forms

text_widget_class = 'form-control'
select_widget_class = 'custom-select'
checkbox_widget_class = 'custom-control-input'

class BootstrapForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        for field_name, field in self.fields.items():

            widget_class = select_widget_class if hasattr(field.widget, 'input_type') and field.widget.input_type == 'select' else text_widget_class
            if hasattr(field.widget, 'input_type') and field.widget.input_type == 'checkbox':
                widget_class = checkbox_widget_class


            if hasattr(self,'required_fields') and field_name in self.required_fields:
                field.required = True

            if 'class' in field.widget.attrs:
                if widget_class not in field.widget.attrs['class']:
                   field.widget.attrs['class'] += ' ' + widget_class
            else:
                field.widget.attrs['class'] = widget_class

            if field_name == 'o':
                # For the ordering input, we set special attributes
                field.widget.attrs['class'] += ' search-field'

            if not 'placeholder' in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label
