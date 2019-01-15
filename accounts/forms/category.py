from django import forms

from accounts.models import Category
from core.forms.BootstrapForm import BootstrapForm


class CategoryForm(forms.ModelForm, BootstrapForm):

    class Meta:
        model = Category
        widgets = {
            'color': forms.TextInput(attrs={'class': 'color-widget'}),
        }
        exclude = []

