from ..integrations.authorization_arena import *


def get_endpoint_response(headers, endpoint):
    url = f"http://localhost:8080/api/json/{endpoint}"
    response = requests.get(url, headers=headers)
    return response.json()


def get_custom_id(person_id):

    headers = get_headers()

    custom = get_endpoint_response(headers, f"person/get/{person_id}")

    return custom['person']['customId']


def get_fighter_custom_id(fighter_id):

    headers = get_headers()

    custom = get_endpoint_response(headers, f"fighter/get/{fighter_id}")

    return get_custom_id(custom['fighter']['personId'])


def get_weight_categories(spor_event_id):

    weight_categories = get_endpoint_response(get_headers(), f"weight-category/{spor_event_id}")['weightCategories']
    categorias = {}

    for category in weight_categories:
        id_categoria = category['id']
        nome = category['shortName']
        categorias[id_categoria] = nome

    return categorias


def get_fights_by_category(event_id, category_id):
    url = f"http://localhost:8080/api/json/fight/{event_id}/bracket/{category_id}"
    r = requests.get(url, headers=get_headers())
    r.raise_for_status()
    return r.json().get("fights", [])


def get_fight(fight_id):
    url = f"http://localhost:8080/api/json/fight/get/{fight_id}"
    r = requests.get(url, headers=get_headers())
    r.raise_for_status()
    return r.json().get("fight", {})

