from django.urls import reverse, resolve

from accounts.forms.entity_collab import EditCollabForm
from payments.forms.FeeComment import FeeCommentForm
from payments.models import FeeComments


class EntityCollabFormMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['add_collab_form'] = EditCollabForm(initial={'entity':self.object})
        context['add_collab_form'].action = reverse('accounts:collab_entity_add')
        context['collabs'] = []
        collabs = self.object.get_active_collaborations()
        if (len(collabs) > 0):

            for collab in collabs:
                form = EditCollabForm(instance=collab)
                form.action = reverse('accounts:collab_entity_update', kwargs={'pk': collab.pk})
                context['collabs'].append(form)


        return context
