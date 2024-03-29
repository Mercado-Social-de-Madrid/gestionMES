# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from social_balance.models import EntitySocialBalance, SocialBalanceBadge, BalanceProcess


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('entity', 'year', 'is_exempt', 'done')

class ProcessAdmin(admin.ModelAdmin):
    list_display = ('account', 'year', 'balance_type')

admin.site.register(EntitySocialBalance, BalanceAdmin)
admin.site.register(SocialBalanceBadge)
admin.site.register(BalanceProcess, ProcessAdmin)