
# coding=utf-8
import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import Group

from core.forms.BootstrapModelForm import BootstrapModelForm
from core.forms.signup import SignUpForm
from core.models import User


class UserForm(SignUpForm, BootstrapModelForm ):

    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)
