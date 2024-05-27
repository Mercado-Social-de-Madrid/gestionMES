import tempfile

import requests
from django.conf import settings
from django.utils import timezone

from accounts.models import Consumer, Provider, Category
from currency.models import CurrencyAppUser


def download_entity_logo(account, logo):
    if account.logo:
        #print('Image already exists')
        return

    logo_url = settings.CURRENCY_SERVER_BASE_URL + logo[1:]
    resp = requests.get(logo_url, stream=True)

    if resp.status_code == requests.codes.ok:
        file_name = logo_url.split("/")[-1]
        tmp = tempfile.NamedTemporaryFile(mode='wb', delete=False)
        tmp.write(resp.raw.read())
        tmp.close()

        with open(tmp.name, 'rb') as f:
            account.logo.save(file_name, f)


def update_categories(account, data):
    if not 'categories' in data or len(data['categories'])==0:
        return

    account.categories.set( Category.objects.filter(pk__in=data['categories']))


def update_social_profile_links(account, data):
    if 'social_profiles' in data and data['social_profiles']:
        for social_profile in data['social_profiles']:
            if social_profile['name'] == "Telegram":
                account.telegram_link = social_profile['url']
            elif social_profile['name'] == "Twitter":
                account.twitter_link = social_profile['url']
            elif social_profile['name'] == "Facebook":
                account.facebook_link = social_profile['url']


def fetch_account(account):
    api_url = '{}api/v1/fetch/'.format(settings.CURRENCY_SERVER_BASE_URL)
    headers = {'Authorization': settings.CURRENCY_SERVER_AUTH_HEADER}

    fetch_info = {
	    "cif": account.cif,
        "email": account.contact_email,
    }
    app_user = CurrencyAppUser.objects.filter(account=account)
    if app_user.exists():
        selected = app_user.first()
        if app_user.count() > 1:
            print('remove duplicate currency users')
            app_user.exclude(pk=selected.pk).delete()  # remove all but first

        if selected.uuid is not None:
            fetch_info['uuid'] = str(selected.uuid)


    r = requests.get(api_url, json=fetch_info, headers=headers)

    if r.ok:
        result = r.json()
        app_user, created = CurrencyAppUser.objects.get_or_create(account=account)
        app_user.cif = account.cif
        app_user.is_pushed = True
        uuid = None

        user = result['user']
        if 'is_registered' in user and user['is_registered']:
            app_user.username = user['email']

        if result['type'] == 'person':
            if account.get_real_instance_class() is not Consumer:
                print('Wrong account type! {} - {}. Cif: {}. Email: {}'.format(result['type'], type(account.get_real_instance_class()), account.cif, account.contact_email))
                return False

            account_data = result['person']
            if 'first_name' in account_data and account_data['first_name']:
                account.first_name = account_data['first_name']
            if 'last_name' in account_data and account_data['last_name']:
                account.last_name = account_data['last_name']
            if 'email' in account_data and account_data['email']:
                account.contact_email = account_data['email']
            uuid = account_data['id']
            account.last_updated = timezone.now()
            account.save()

        elif result['type'] == 'entity':
            if account.get_real_instance_class() is not Provider:
                print('Wrong account type! {} - {}. Cif: {}. Email: {}'.format(result['type'], type(account.get_real_instance_class()), account.cif, account.contact_email))
                return False

            account_data = result['entity']
            if 'name' in account_data and account_data['name']:
                account.name = account_data['name']
            if 'description' in account_data and account_data['description']:
                account.description = account_data['description']
            if 'short_description' in account_data and account_data['short_description']:
                account.short_description = account_data['short_description']
            if 'webpage_link' in account_data and account_data['webpage_link']:
                account.webpage_link = account_data['webpage_link']
            if 'longitude' in account_data and account_data['longitude']:
                account.longitude = account_data['longitude']
            if 'latitude' in account_data and account_data['latitude']:
                account.latitude = account_data['latitude']
            if 'address' in account_data and account_data['address']:
                account.public_address = account_data['address']
            if 'profile_image' in account_data and account_data['profile_image']:
                download_entity_logo(account, account_data['profile_image'])

            update_categories(account, account_data)
            update_social_profile_links(account, account_data)

            uuid = account_data['id']
            account.last_updated = timezone.now()
            account.save()

        app_user.uuid = uuid
        app_user.save()
        return True

    else:
        return r.status_code


def fetch_guest_account(account):
    api_url = '{}api/v1/fetch/'.format(settings.CURRENCY_SERVER_BASE_URL)
    headers = {'Authorization': settings.CURRENCY_SERVER_AUTH_HEADER}

    fetch_info = {
        "cif": account.guest_reference,
        "email": account.contact_email,
    }
    app_user = CurrencyAppUser.objects.filter(guest_account=account)
    if app_user.exists():
        selected = app_user.first()
        if app_user.count() > 1:
            print('remove duplicate currency users')
            app_user.exclude(pk=selected.pk).delete()  # remove all but first

        if selected.uuid is not None:
            fetch_info['uuid'] = str(selected.uuid)

    r = requests.get(api_url, json=fetch_info, headers=headers)

    if r.ok:
        result = r.json()
        app_user, created = CurrencyAppUser.objects.get_or_create(guest_account=account)
        app_user.is_pushed = True
        user = result['user']
        if 'is_registered' in user and user['is_registered']:
            app_user.username = user['email']

        account_data = result['person']
        if 'first_name' in account_data and account_data['first_name']:
            account.first_name = account_data['first_name']
        if 'last_name' in account_data and account_data['last_name']:
            account.last_name = account_data['last_name']
        if 'email' in account_data and account_data['email']:
            account.contact_email = account_data['email']

        account.save()
        app_user.uuid = account_data['id']
        app_user.save()
        return True
    else:
        return r.status_code


def fetch_intercoop_account(account):
    api_url = '{}api/v1/fetch/'.format(settings.CURRENCY_SERVER_BASE_URL)
    headers = {'Authorization': settings.CURRENCY_SERVER_AUTH_HEADER}

    fetch_info = {
        "cif": account.cif,
        "email": account.contact_email,
    }

    app_user = CurrencyAppUser.objects.filter(intercoop_account=account)
    if app_user.exists():
        selected = app_user.first()
        if app_user.count() > 1:
            print('remove duplicate currency users')
            app_user.exclude(pk=selected.pk).delete()  # remove all but first

        if selected.uuid is not None:
            fetch_info['uuid'] = str(selected.uuid)

    r = requests.get(api_url, json=fetch_info, headers=headers)

    if r.ok:
        result = r.json()
        app_user, created = CurrencyAppUser.objects.get_or_create(intercoop_account=account)
        app_user.is_pushed = True
        user = result['user']
        if 'is_registered' in user and user['is_registered']:
            app_user.username = user['username']

        if not 'person' in result or not result['person']:
            return False

        account_data = result['person']
        if 'name' in account_data and account_data['name']:
            account.first_name = account_data['name']
        if 'surname' in account_data and account_data['surname']:
            account.last_name = account_data['surname']
        if 'email' in account_data and account_data['email']:
            account.contact_email = account_data['email']

        account.last_updated = timezone.now()
        account.save()
        app_user.uuid = account_data['id']
        app_user.save()
        return True
    else:
        return r.status_code
