from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWABLE_VALUES = ("GMAPS_APIKEY", "MAIN_PAGE_TITLE", "INITIAL_LATITUDE", "INITIAL_LONGITUDE", "BASESITE_URL", "INLINE_INPUT_SEPARATOR")

# settings value (based on https://stackoverflow.com/a/21593607)
@register.simple_tag
def settings_value(name):
    if name in ALLOWABLE_VALUES:
        return mark_safe(getattr(settings, name, ''))
    return ''