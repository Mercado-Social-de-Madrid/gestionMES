import django_filters
from django.conf import settings


class MemberTypeFilter(django_filters.ChoiceFilter):

    def __init__(self, *args, **kwargs):
        django_filters.ChoiceFilter.__init__(self, choices=settings.MEMBER_TYPES, *args, **kwargs)

    def filter(self, qs, value):
        if value not in (None, ''):
            qs = qs.filter(account__member_type=value)
        return qs
