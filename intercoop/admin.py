# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from intercoop.models import IntercoopEntity, IntercoopAccount


class IntercoopAccountAdmin(admin.ModelAdmin):
    list_display = ('active', 'display_name', 'entity')
    search_fields = (
        'cif',
    )


admin.site.register(IntercoopEntity)
admin.site.register(IntercoopAccount, IntercoopAccountAdmin)