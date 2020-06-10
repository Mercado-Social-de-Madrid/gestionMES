# coding=utf-8
from django.urls import reverse
from menu import Menu, MenuItem
from django.utils.translation import gettext as _

from core.menu_item import PermissionsMenuItem
from management.menus import MANAGEMENT_MENU_WEIGHT

PAYMENTS_MENU_WEIGHT = 200

Menu.add_item("main",PermissionsMenuItem(_("Procesos"), reverse('bpm:list'), weight=MANAGEMENT_MENU_WEIGHT+30, icon="dns"))