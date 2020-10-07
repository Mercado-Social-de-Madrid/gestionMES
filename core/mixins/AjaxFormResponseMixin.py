from django.http import JsonResponse
from django.views import View

class AjaxFormResponseMixin(object):
    """
    A mixin that can be used to render a different templates based in the kind of request (Ajax or not).
    """

    def form_valid(self, form):
        if self.request.is_ajax():
            return JsonResponse({
                'success': True,
                'results': form.results if form.results else None,
                'success_url': self.get_success_url()
            })
        else:
            return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            response = JsonResponse({
                'success': False,
                'form_errors': form.errors
            })
            response.status_code = 400
            return response
        else:
            return super().form_invalid(form)