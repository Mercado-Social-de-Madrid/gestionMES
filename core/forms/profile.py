# coding=utf-8
import datetime
from dateutil.relativedelta import relativedelta
from django import forms

from core.models import User


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'readonly':True }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
        }
