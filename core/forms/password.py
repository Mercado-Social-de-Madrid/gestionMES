




# coding=utf-8
import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.forms import PasswordChangeForm
from django import forms

from core.forms.BootstrapModelForm import BootstrapModelForm
from core.models import User


class PasswordForm(BootstrapModelForm, PasswordChangeForm ):
    pass

