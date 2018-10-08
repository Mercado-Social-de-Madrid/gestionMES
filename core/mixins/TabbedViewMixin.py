from django.urls import resolve


class TabbedViewMixin(object):
    """
    A mixin to add to the view context the active tab we want to show
    """

    default_tab = None
    available_tabs = None

    def get_context_data(self, **kwargs):
        context = super(TabbedViewMixin, self).get_context_data(**kwargs)
        edit_tab = self.request.GET.get('tab', default=self.default_tab)
        if edit_tab is not None:
            if self.available_tabs is not None and edit_tab not in self.available_tabs:
                edit_tab = self.default_tab
            context[edit_tab + '_tab'] = True

        return context
