# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from accounts.models import LegalForm, Category, SignupProcess, Provider, Consumer, DeletionProcess, Colaborator


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('cif', 'name', 'business_name')
    search_fields = (
        'name',
    )

admin.site.register(LegalForm)
admin.site.register(Category)
admin.site.register(SignupProcess)
admin.site.register(DeletionProcess)
admin.site.register(Consumer)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Colaborator, ProviderAdmin)