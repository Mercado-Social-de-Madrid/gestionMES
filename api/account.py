from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource

from accounts.models import Account, INITIAL_PAYMENT, ACTIVE, PENDING_PAYMENT


class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        resource_name = 'account'
        list_allowed_methods = []
        detail_allowed_methods = ['get']


    def obj_get(self, bundle, **kwargs):
        pk = kwargs['pk']
        account = Account.objects.filter(cif=pk)
        if account.exists():
            return account.first()
        else:
            raise NotFound


    def dehydrate(self, bundle):
        user = bundle.obj
        bundle.data['is_active'] = user.status == ACTIVE or user.status == INITIAL_PAYMENT or user.status == PENDING_PAYMENT
        return bundle