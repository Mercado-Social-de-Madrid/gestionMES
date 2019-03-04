import requests
from django.conf import settings

# TODO: Definir la ciudad concreta de otra forma
CITY_ID = 'mad'

def post_entity(entity):
    api_url = '{}api/v1/preregister/'.format(settings.CURRENCY_SERVER_BASE_URL)

    entity_dict = {
        "address": entity.address,
	    "bonus_percent_entity": entity.bonus_percent_entity,
        "bonus_percent_general": entity.bonus_percent_general,
	    "cif": entity.cif,
	    "description": entity.description,
	    "email": entity.contact_email,
	    "facebook_link": entity.facebook_link,
	    "instagram_link": entity.instagram_link,
	    "latitude": entity.latitude,
	    "legal_form": entity.legal_form.title,
	    "longitude": entity.longitude,
	    "max_percent_payment": entity.max_percent_payment,
	    "name": entity.name,
	    "num_workers": entity.num_workers,
	    "short_description": entity.short_description,
	    "telegram_link": entity.telegram_link,
	    "twitter_link": entity.twitter_link,
	    "webpage_link": entity.webpage_link,
        "city": CITY_ID,
    }


    r = requests.post(api_url, json={
        'email': entity.contact_email,
        'entity': entity_dict
    })


    if r.ok:
        result = r.json()
        uuid = result['entity']['id']
        return True, uuid
    else:
        return False, None


def post_consumer(consumer):
    api_url = '{}api/v1/preregister/'.format(settings.CURRENCY_SERVER_BASE_URL)
    consumer_dict = {
        "address": consumer.address,
        "nif": consumer.cif,
        "email": consumer.contact_email,
        "name": consumer.first_name,
        "surname": consumer.last_name,
        "is_guest_account": False,
        "city": CITY_ID,
    }

    r = requests.post(api_url, json={
        'email': consumer.contact_email,
        'person': consumer_dict
    })

    if r.ok:
        result = r.json()
        uuid = result['person']['id']
        return True, uuid
    else:
        return False, None


def post_guest(guest):
    api_url = '{}api/v1/preregister/'.format(settings.CURRENCY_SERVER_BASE_URL)
    guest_dict = {
        "address": guest.address,
        "nif": guest.cif,
        "email": guest.contact_email,
        "name": guest.first_name,
        "surname": guest.last_name,
        "is_guest_account": True,
        "city": CITY_ID,
    }

    r = requests.post(api_url, json={
        'email': guest.contact_email,
        'person': guest_dict
    })
    print r.status_code

    if r.ok:
        result = r.json()
        uuid = result['person']['id']
        return True, uuid
    else:
        return False, None
