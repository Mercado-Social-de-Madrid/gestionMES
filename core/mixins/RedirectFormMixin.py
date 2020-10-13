from django.views.generic import FormView


class RedirectFormMixin(FormView):

    def get_success_url(self):
        if self.redirect_url:
            return self.redirect_url
        else:
            return super().get_success_url()

    def form_valid(self, form):
        self.redirect_url = form.cleaned_data.get('redirect_to')
        return super().form_valid(form)

