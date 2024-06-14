# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from django.utils.translation import gettext_lazy as _

from payments.models import FeeRange
from settings import constants


def add_if_empty(model, category, key, int_value=None, bool_value=None, str_value=None, float_value=None):
    try:
        model.objects.get(key=key)
    except model.DoesNotExist:
        settings_prop = model(key=key,
                             category=category,
                             str_value=str_value,
                             bool_value=bool_value,
                             int_value=int_value,
                             float_value=float_value)
        settings_prop.save()

def add_initial_settings(apps, schema_editor):

    props = apps.get_model("settings", "SettingProperties")

    add_if_empty(props, constants.SETTING_CATEGORY_PAYMENTS, constants.PAYMENTS_CURRENT_FEECHARGES_YEAR, int_value=settings.CURRENT_FEECHARGES_YEAR)
    add_if_empty(props, constants.SETTING_CATEGORY_PAYMENTS, constants.PAYMENTS_DEFAULT_CONSUMER_FEE, float_value=settings.DEFAULT_CONSUMER_FEE)
    add_if_empty(props, constants.SETTING_CATEGORY_PAYMENTS, constants.PAYMENTS_DEFAULT_PROVIDER_FEE, float_value=settings.DEFAULT_PROVIDER_FEE)
    add_if_empty(props, constants.SETTING_CATEGORY_PAYMENTS, constants.PAYMENTS_DEFAULT_CONSUMER_SOCIAL_CAPITAL, float_value=settings.DEFAULT_CONSUMER_SOCIAL_CAPITAL)
    add_if_empty(props, constants.SETTING_CATEGORY_PAYMENTS, constants.PAYMENTS_DEFAULT_PROVIDER_SOCIAL_CAPITAL, float_value=settings.DEFAULT_PROVIDER_SOCIAL_CAPITAL)
    add_if_empty(props, constants.SETTING_CATEGORY_PAYMENTS, constants.PAYMENTS_DEFAULT_SPECIAL_FEE, float_value=settings.DEFAULT_SPECIAL_FEE)

    add_if_empty(props, constants.SETTING_CATEGORY_BALANCE, constants.BALANCE_CURRENT_YEAR, int_value=settings.CURRENT_BALANCE_YEAR)

    Account = apps.get_model("accounts", "Account")
    member = Account.objects.exclude(member_id__isnull=True).order_by('member_id').last()
    last_member_id = int(member.member_id)

    IntercoopAccount = apps.get_model("intercoop", "IntercoopAccount")
    member = IntercoopAccount.objects.exclude(member_id__isnull=True).order_by('member_id').last()
    last_intercoop_id = int(member.member_id[6:])

    add_if_empty(props, constants.SETTING_CATEGORY_ACCOUNTS, constants.ACCOUNTS_LAST_MEMBER_ID, int_value=last_member_id)
    add_if_empty(props, constants.SETTING_CATEGORY_ACCOUNTS, constants.ACCOUNTS_LAST_INTERCOOP_ID, int_value=last_intercoop_id)

class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
        ('accounts', '0045_account_member_id'),
        ('intercoop', '0009_intercoopaccount_member_id')
    ]

    operations = [
        migrations.RunPython(add_initial_settings),
    ]
