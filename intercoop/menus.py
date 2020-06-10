# coding=utf-8
from django.urls import reverse
from django.utils.translation import gettext as _
from menu import Menu

from accounts.menus import ACCOUNTS_MENU_WEIGHT
from core.menu_item import PermissionsMenuItem

Menu.add_item("main",PermissionsMenuItem(_("Intercooperación"), reverse('intercoop:accounts_list'), weight=ACCOUNTS_MENU_WEIGHT+60, icon="extension"))
