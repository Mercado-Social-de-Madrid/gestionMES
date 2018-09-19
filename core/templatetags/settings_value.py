from django import template
from django.conf import settings

register = template.Library()

ALLOWABLE_VALUES = ("GMAPS_APIKEY", "MAIN_PAGE_TITLE", "INITIAL_LATITUDE", "INITIAL_LONGITUDE", "BASESITE_URL")

# settings value (based on https://stackoverflow.com/a/21593607)
@register.simple_tag
def settings_value(name):
    if name in ALLOWABLE_VALUES:
        return getattr(settings, name, '')
    return ''