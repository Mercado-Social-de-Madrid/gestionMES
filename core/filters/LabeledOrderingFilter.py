import django_filters
from django.utils.translation import gettext as _

class LabeledOrderingFilter(django_filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('empty_label', _('Ordenar por...'))
        super(LabeledOrderingFilter, self).__init__(*args, **kwargs)
