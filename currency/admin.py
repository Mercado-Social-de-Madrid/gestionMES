# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from currency.models import GuestInvitation, GuestAccount

admin.site.register(GuestInvitation)
admin.site.register(GuestAccount)
