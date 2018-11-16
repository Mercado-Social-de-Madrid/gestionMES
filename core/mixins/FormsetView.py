from django.urls import resolve
from django.views.generic.edit import FormMixin


class FormsetView(FormMixin):
    """
    A mixin to manage a view with formsets
    """

    update_formset_after_save = False

    def get_context_data(self, **kwargs):
        context = super(FormsetView, self).get_context_data(**kwargs)
        context['formsets'] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        return []

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        for formset in named_formsets.values():
            formset_instance = formset(self.request.POST, self.request.FILES)
            if not formset_instance.is_valid():
                errors = formset_instance.errors
                print errors
                print 'invalid formset!!'
                return self.form_invalid(form)


        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_instance = formset(self.request.POST)
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset_instance, self.object)
            else:
                formset_instance.save()

        return super(FormsetView, self).form_valid(form)