from tastypie.api import Api

from api.account import AccountResource, GuestAccountResource


def get_api(version_name):

    api = Api(api_name=version_name)
    api.register(AccountResource())
    api.register(GuestAccountResource())

    return api