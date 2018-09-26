from django.urls import resolve


class ListItemUrlMixin(object):
    """
    A mixin to add the detail url for an object, constructing it with its namespace
    """

    objects_url_name = None

    def get_context_data(self, **kwargs):
        context = super(ListItemUrlMixin, self).get_context_data(**kwargs)

        if self.objects_url_name != None:
            namespace = resolve(self.request.path).namespace
            context['object_url_name'] = '{}:{}'.format(namespace, self.objects_url_name)
        return context