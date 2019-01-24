# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from accounts.models import LegalForm, Category, SignupProcess, Provider, Consumer

admin.site.register(LegalForm)
admin.site.register(Category)
admin.site.register(SignupProcess)
admin.site.register(Consumer)
admin.site.register(Provider)