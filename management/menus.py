# coding=utf-8
from django.urls import reverse
from menu import Menu, MenuItem
from django.utils.translation import gettext as _

from core.menu_item import PermissionsMenuItem

MANAGEMENT_MENU_WEIGHT = 0

Menu.add_item("main", PermissionsMenuItem(_("Administración"), '#', permissions=None, weight=MANAGEMENT_MENU_WEIGHT, is_title=True))
Menu.add_item("main",PermissionsMenuItem(_("Usuarios"), reverse('management:users_list'), weight=MANAGEMENT_MENU_WEIGHT+10, icon="face"))
Menu.add_item("main",PermissionsMenuItem(_("Comisiones"), reverse('management:commission_list'), weight=MANAGEMENT_MENU_WEIGHT+20, icon="group"))
