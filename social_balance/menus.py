# coding=utf-8
from django.urls import reverse
from menu import Menu, MenuItem
from django.utils.translation import gettext as _

from core.menu_item import PermissionsMenuItem
from management.menus import MANAGEMENT_MENU_WEIGHT

PAYMENTS_MENU_WEIGHT = 200

Menu.add_item("main", PermissionsMenuItem(_("Contabilidad"), '#', weight=PAYMENTS_MENU_WEIGHT, is_title=True))
Menu.add_item("main",PermissionsMenuItem(_("Cuotas anuales"), reverse('payments:annual_feecharges', kwargs={'year':2020}), weight=PAYMENTS_MENU_WEIGHT+10, icon="menu_book"))
Menu.add_item("main",PermissionsMenuItem(_("Pagos"), reverse('payments:payments_list')+'?status=activa', weight=PAYMENTS_MENU_WEIGHT+20, icon="receipt"))
Menu.add_item("main",PermissionsMenuItem(_("Remesas (SEPA)"), reverse('payments:sepa_list'), weight=PAYMENTS_MENU_WEIGHT+30, icon="library_books"))
Menu.add_item("main",PermissionsMenuItem(_("Movimientos de tarjeta"), reverse('payments:card_payments_list'), weight=PAYMENTS_MENU_WEIGHT+40, icon="credit_card"))
