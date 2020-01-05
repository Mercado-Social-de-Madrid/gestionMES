from django.urls import reverse, resolve

from payments.forms.FeeComment import FeeCommentForm
from payments.models import FeeComments


class FeeCommentsMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view = resolve(self.request.path)
        view_redirect = '{}:{}'.format(view.namespace, view.url_name )
        print(view_redirect)
        form = FeeCommentForm(initial={
            'account': self.object,
            'redirect_to': reverse(view_redirect, kwargs={'pk': self.object.pk})
        })
        context['comment_form'] = form
        context['fee_comments'] = FeeComments.objects.filter(account=self.object).order_by('-timestamp')

        return context
