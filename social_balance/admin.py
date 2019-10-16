# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from social_balance.models import EntitySocialBalance, SocialBalanceBadge


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('entity', 'year', 'is_exempt', 'done')

admin.site.register(EntitySocialBalance, BalanceAdmin)
admin.site.register(SocialBalanceBadge)