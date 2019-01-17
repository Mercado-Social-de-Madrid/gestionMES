# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from accounts.models import LegalForm, Category, SignupProcess, Provider
from payments.models import FeeRange, PendingPayment

admin.site.register(FeeRange)
admin.site.register(PendingPayment)