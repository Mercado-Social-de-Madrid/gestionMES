# coding=utf-8
from django.urls import reverse
from menu import Menu
from django.utils.translation import gettext as _

from core.menu_item import PermissionsMenuItem

BALANCE_MENU_WEIGHT = 300

Menu.add_item("main", PermissionsMenuItem(_("Balance social"), '#',
          permissions=['social_balance.mespermission_can_view_social_balances',
                       'social_balance.mespermission_can_edit_social_balances',
                       'social_balance.mespermission_can_view_social_badges',
                       'social_balance.mespermission_can_create_social_badges',
                       'social_balance.mespermission_can_manage_balance_process',
                       'social_balance.mespermission_can_add_balance_comments',
                       'social_balance.mespermission_can_view_balance_process'
                       ], weight=BALANCE_MENU_WEIGHT, is_title=True))
Menu.add_item("main",PermissionsMenuItem(_("Sellos (plantilla)"), reverse('balance:badge_list'), weight=BALANCE_MENU_WEIGHT+10, icon="palette"))
Menu.add_item("main",PermissionsMenuItem(_("Datos anuales"), reverse('balance:balance'), weight=BALANCE_MENU_WEIGHT+20, icon="art_track"))
Menu.add_item("main",PermissionsMenuItem(_("Procesos balance"), reverse('balance:process_list'), weight=BALANCE_MENU_WEIGHT+30, icon="explore"))
