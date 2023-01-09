# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from accounts.models import LegalForm, Category, SignupProcess, Provider, Consumer, DeletionProcess, Colaborator, \
    Collaboration, EntityCollaboration, SocialCapital


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('cif', 'name', 'business_name')
    search_fields = (
        'name',
    )


class ColabAdmin(admin.ModelAdmin):
    list_display = ('entity', 'collaboration', 'started')


class SocialCapitalAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'paid_type', 'paid', 'paid_timestamp', 'returned', 'returned_timestamp')


admin.site.register(LegalForm)
admin.site.register(Category)
admin.site.register(SignupProcess)
admin.site.register(DeletionProcess)
admin.site.register(Consumer)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Colaborator, ProviderAdmin)
admin.site.register(Collaboration)
admin.site.register(EntityCollaboration, ColabAdmin)
admin.site.register(SocialCapital, SocialCapitalAdmin)