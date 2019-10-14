


class SignupFormMixin(object):

    def get_form_kwargs(self):
        kw = super(SignupFormMixin, self).get_form_kwargs()
        kw['from_app'] = self.request.GET.get('from_app', False)
        return kw