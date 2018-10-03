# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

from management.models import Comission


class GroupInline(admin.StackedInline):
    model = Comission
    can_delete = False
    verbose_name_plural = 'Comisiones'


class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupInline, )


# Re-register GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comission)