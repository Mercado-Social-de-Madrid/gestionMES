# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from currency.models import GuestInvitation, GuestAccount, CurrencyAppUser


class AppUserAdmin(admin.ModelAdmin):
    list_display = ('account', 'username', 'cif')
    search_fields = (
        'cif',
    )


admin.site.register(GuestInvitation)
admin.site.register(GuestAccount)
admin.site.register(CurrencyAppUser, AppUserAdmin)