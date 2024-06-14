from django.contrib import admin

from settings.models import SettingProperties


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('key',
                    'category',
                    'description',
                    'str_value',
                    'int_value',
                    'bool_value',
                    'float_value')


admin.site.register(SettingProperties, SettingsAdmin)
