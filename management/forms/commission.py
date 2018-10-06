from django import forms
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext as _

from core.forms.BootstrapModelForm import BootstrapModelForm
from management.models import Comission


class CommissionForm(forms.ModelForm, BootstrapModelForm):

    group_name = forms.CharField(label=_('Nombre'), required=True)
    permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.filter(codename__startswith='mespermission'))

    class Meta:
        model = Comission
        exclude = ['group']
        widgets = {
            'label_color': forms.TextInput(attrs={'class': 'color-widget'}),
        }

    # Overriding __init__ here allows us to provide initial data for permissions
    def __init__(self, *args, **kwargs):
        # Only in case we build the form from an instance
        # (otherwise, 'toppings' list should be empty)
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects
            # a list of primary key for the selected data.
            initial['group_name'] = kwargs['instance'].group.name
            initial['permissions'] = [t.pk for t in kwargs['instance'].group.permissions.all()]

        forms.ModelForm.__init__(self, *args, **kwargs)

    # Overriding save allows us to process the value of 'toppings' field
    def save(self, commit=True):

        is_new = self.instance.pk is None
        group_name = self.cleaned_data['group_name']
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the permissions to the group
           instance.group.permissions.clear()
           instance.group.permissions.add(*self.cleaned_data['permissions'])
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            if is_new:
                # Create the associated group
                group = Group.objects.create(name=group_name)
                instance.group = group

            instance.group.name = group_name
            instance.save()
            self.save_m2m()

        return instance