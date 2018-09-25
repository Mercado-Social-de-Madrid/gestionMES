from django.urls import resolve
from django.views.generic.base import TemplateResponseMixin


class ListItemUrlMixin(object):
    """
    A mixin that can be used to render a different templates based in the kind of request (Ajax or not).
    """

    objects_url_name = None

    def get_context_data(self, **kwargs):
        context = super(ListItemUrlMixin, self).get_context_data(**kwargs)

        if self.objects_url_name != None:
            namespace = resolve(self.request.path).namespace
            context['object_url_name'] = '{}:{}'.format(namespace, self.objects_url_name)
        return context