from django.http import HttpResponseRedirect
from django.views.generic import FormView


class RedirectFormMixin(FormView):

    def get_success_url(self):
        if self.redirect_url:
            return self.redirect_url
        else:
            return super().get_success_url()

    def form_valid(self, form, direct_redirect=False):
        self.redirect_url = form.cleaned_data.get('redirect_to')
        if direct_redirect:
            return HttpResponseRedirect(self.redirect_url)
        else:
            return super().form_valid(form)
