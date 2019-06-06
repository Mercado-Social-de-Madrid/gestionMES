from django.db.models import ManyToOneRel
from django.urls import resolve


class ModelFieldsViewMixin(object):
    """
    A mixin to add the detail url for an object, constructing it with its namespace
    """

    objects_url_name = None
    __fields = None

    # Method to only load CSV fields and inspect class once
    @classmethod
    def load_fields(cls, instance):
        if not cls.__fields:
            cls.__fields = cls.model._meta.get_fields()


    def __init__(self, *args, **kwargs):
        super(ModelFieldsViewMixin, self).__init__(*args, **kwargs)
        self.load_fields(self)


    def get_context_data(self, **kwargs):
        context = super(ModelFieldsViewMixin, self).get_context_data(**kwargs)
        values = []
        for field in self.__fields:
            if not isinstance(field, ManyToOneRel):
                values.append({
                    'label': field.verbose_name if hasattr(field, 'verbose_name') else field.attname,
                    'id': field.attname,
                    'value': getattr(self.object, field.attname)
                })

        context['obj_field_values'] = values
        print values
        return context