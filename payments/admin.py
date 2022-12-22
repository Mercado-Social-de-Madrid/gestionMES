# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from payments.models import FeeRange, PendingPayment, CardPayment, SepaPaymentsBatch, BankBICCode, AnnualFeeCharges, \
    AccountAnnualFeeCharge


class BICAdmin(admin.ModelAdmin):
    list_display = ('bank_code', 'bank_name', 'bic_code',  )
    search_fields = (
        'bank_code',
    )

class AccountAnnualFeeChargeAdmin(admin.ModelAdmin):
    list_display = ('cif',)
    search_fields = (
        'cif',
    )

admin.site.register(FeeRange)
admin.site.register(PendingPayment)
admin.site.register(CardPayment)
admin.site.register(SepaPaymentsBatch)
admin.site.register(BankBICCode, BICAdmin)
admin.site.register(AnnualFeeCharges)
admin.site.register(AccountAnnualFeeCharge, AccountAnnualFeeChargeAdmin)
