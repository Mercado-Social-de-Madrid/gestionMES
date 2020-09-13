# coding=utf-8
from django.urls import reverse
from menu import Menu, MenuItem
from django.utils.translation import gettext as _

from core.menu_item import PermissionsMenuItem
from management.menus import MANAGEMENT_MENU_WEIGHT

ACCOUNTS_MENU_WEIGHT = 100

Menu.add_item("main", PermissionsMenuItem(_("Socias"), '#', weight=ACCOUNTS_MENU_WEIGHT, is_title=True))
Menu.add_item("main",PermissionsMenuItem(_("Acogidas"), reverse('accounts:signup_list')+'?status=', weight=ACCOUNTS_MENU_WEIGHT+10, icon="call_received"))
Menu.add_item("main",PermissionsMenuItem(_("Proveedoras"), reverse('accounts:providers_list')+'?status=activa', weight=ACCOUNTS_MENU_WEIGHT+20, icon="store"))
Menu.add_item("main",PermissionsMenuItem(_("Consumidoras"), reverse('accounts:consumers_list'), weight=ACCOUNTS_MENU_WEIGHT+30, icon="directions_walk"))

Menu.add_item("main",PermissionsMenuItem(_("Entidades esp."), reverse('accounts:entity_list'), weight=ACCOUNTS_MENU_WEIGHT+50, icon="grade"))
Menu.add_item("main",PermissionsMenuItem(_("Bajas"), reverse('accounts:deletion_list'), weight=ACCOUNTS_MENU_WEIGHT+70, icon="trending_down"))

Menu.add_item("main",PermissionsMenuItem(_("Categorías"), reverse('accounts:category_list'), weight=MANAGEMENT_MENU_WEIGHT+50, icon="label"))
Menu.add_item("main",PermissionsMenuItem(_("Informes"), reverse('accounts:accounts_report'), weight=MANAGEMENT_MENU_WEIGHT+60, icon="assessment"))
