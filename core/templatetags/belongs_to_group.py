from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def belongs_to_group(user, group_name):
    try:
        group =  Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False

    return group in user.groups.all()