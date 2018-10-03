# coding=utf-8
import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.forms import UserCreationForm
from django import forms

from core.models import User


class SignUpForm(UserCreationForm):


    class Meta:
        model = User
        fields = ("username", 'email', 'first_name', 'last_name')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            self.add_error('username', u'El nombre de usuario "%s" ya está en uso.' % username)
        return username
