from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tastypie.exceptions import NotFound
from tastypie.http import HttpGone, HttpMultipleChoices, HttpBadRequest, HttpCreated
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from accounts.models import Account, INITIAL_PAYMENT, ACTIVE, PENDING_PAYMENT
from currency.models import GuestInvitation, GuestAccount


class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        resource_name = 'account'
        list_allowed_methods = []
        excludes = ['iban_code', 'pay_by_debit']
        detail_allowed_methods = ['get', 'post']

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>[\w0-9/-]*)/invite%s$" % (
            self._meta.resource_name, trailing_slash()), self.wrap_view('invite'), name="api_invite"),
        ]

    def invite(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        email = data.get('email', '')
        if not email:
            return HttpBadRequest()

        try:
            bundle = self.build_bundle(data={'pk': kwargs['pk']}, request=request)
            account = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
            invite = GuestInvitation.objects.invite_user(account=account, email=email)

            return self.create_response(
                request, {'token':invite.token},
                response_class = HttpCreated)

        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")



    def obj_get(self, bundle, **kwargs):
        pk = kwargs['pk']
        account = Account.objects.filter(cif=pk)
        if account.exists():
            return account.first()
        else:
            account = GuestAccount.objects.filter(cif=pk)
            if account.exists():
                return account.first()
            else:
                raise NotFound


    def dehydrate(self, bundle):
        user = bundle.obj
        bundle.data['is_active'] = user.status == ACTIVE or user.status == INITIAL_PAYMENT or user.status == PENDING_PAYMENT
        return bundle