from tastypie.api import Api

from api.account import AccountResource


def get_api(version_name):

    api = Api(api_name=version_name)
    api.register(AccountResource())

    return api