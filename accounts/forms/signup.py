from django import forms

from core.forms.BootstrapForm import BootstrapForm


class BaseSignupForm(forms.ModelForm, BootstrapForm):
    check_privacy_policy = forms.BooleanField(required=True,
                                              widget=forms.CheckboxInput(attrs={'class':'custom-control-input'}))

    newsletter_check = forms.BooleanField(required=False,
                                              widget=forms.CheckboxInput(attrs={'class':'custom-control-input'}))

    from_app = forms.BooleanField(required=False, widget=forms.HiddenInput())


    def __init__(self, *args, **kwargs):
        from_app = kwargs.pop('from_app', False)
        if kwargs.get('initial', None) is not None and 'from_app' in kwargs['initial']:
                del (kwargs['initial']['from_app'])

        super().__init__(*args, **kwargs)
        self.fields['from_app'].initial = from_app
