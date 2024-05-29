import requests
from django.conf import settings


def post_entity(entity):
    api_url = '{}api/v1/preregister/'.format(settings.CURRENCY_SERVER_BASE_URL)
    headers = {'Authorization': settings.CURRENCY_SERVER_AUTH_HEADER}

    entity_dict = {
	    "cif": entity.cif,
	    "name": entity.name,
        "member_id": entity.member_id,
	    "description": entity.description,
	    "short_description": entity.short_description,
	    "email": entity.contact_email,
        "contact_phone": entity.contact_phone,
        "address": entity.public_address,
        "city": entity.city,
	    "latitude": entity.latitude,
	    "longitude": entity.longitude,
	    "legal_form": entity.legal_form.title,
	    "num_workers": entity.num_workers,
	    "telegram_link": entity.telegram_link,
	    "twitter_link": entity.twitter_link,
	    "webpage_link": entity.webpage_link,
	    "facebook_link": entity.facebook_link,
	    "instagram_link": entity.instagram_link,
        "categories": [str(cat.id) for cat in entity.categories.all()]
    }


    r = requests.post(api_url,
                      json={
                          'email': entity.contact_email,
                          'entity': entity_dict
                      },
                      headers=headers)


    if r.ok:
        result = r.json()
        uuid = result['entity']['id']
        return True, uuid
    else:
        print("post_entity error. Status code {}, message: {}".format(r.status_code, r.text))
        return False, None


def post_consumer(consumer):
    api_url = '{}api/v1/preregister/'.format(settings.CURRENCY_SERVER_BASE_URL)
    headers = {'Authorization': settings.CURRENCY_SERVER_AUTH_HEADER}
    consumer_dict = {
        "cif": consumer.cif,
        "member_id": consumer.member_id,
        "name": consumer.first_name,
        "surname": consumer.last_name,
        "email": consumer.contact_email,
        "contact_phone": consumer.contact_phone,
        "address": consumer.address,
        "city": consumer.city,
    }

    r = requests.post(api_url,
                      json={
                          'email': consumer.contact_email,
                            'person': consumer_dict
                      },
                      headers=headers)

    if r.ok:
        result = r.json()
        uuid = result['person']['id']
        return True, uuid
    else:
        print("post_consumer error. Status code {}, message: {}".format(r.status_code, r.text))
        return False, None


def post_intercoop(account):
    api_url = '{}api/v1/preregister/'.format(settings.CURRENCY_SERVER_BASE_URL)
    headers = {'Authorization': settings.CURRENCY_SERVER_AUTH_HEADER}
    consumer_dict = {
        "cif": account.cif,
        "member_id": account.member_id,
        "name": account.first_name,
        "surname": account.last_name,
        "email": account.contact_email,
        "contact_phone": account.contact_phone,
        "address": account.address,
        "city": account.city,
        "is_intercoop": True,
    }

    r = requests.post(api_url,
                      json={
                          'email': account.contact_email,
                          'person': consumer_dict
                      },
                      headers=headers)

    if r.ok:
        result = r.json()
        uuid = result['person']['id']
        return True, uuid
    else:
        return False, None


# No longer syncing in new HA, consider remove
def post_guest(guest):
    api_url = '{}api/v1/preregister/'.format(settings.CURRENCY_SERVER_BASE_URL)
    headers = {'Authorization': settings.CURRENCY_SERVER_AUTH_HEADER}
    guest_dict = {
        "nif": str(guest.guest_reference),
        "email": guest.contact_email,
        "name": guest.first_name,
        "expiration_date": guest.expiration_date.strftime("%Y-%m-%d %H:%M:%S"),
        "surname": guest.last_name,
        "is_guest_account": True,
        "city": settings.CITY_ID,
    }
    if guest.address:
        guest_dict["address"] = guest.address

    r = requests.post(api_url,
                      json={
                          'email': guest.contact_email,
                          'person': guest_dict
                      },
                      headers=headers)
    print(r.status_code)

    if r.ok:
        result = r.json()
        uuid = result['person']['id']
        return True, uuid
    else:
        return False, None


