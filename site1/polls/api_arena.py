from .authorization_arena import *


def get_endpoint_response(headers, endpoint):
    url = f"http://localhost:8080/api/json/{endpoint}"
    response = requests.get(url, headers=headers)
    return response.json()


def get_custom_id(person_id):

    headers = get_headers()

    custom = get_endpoint_response(headers, f"person/get/{person_id}")

    print(custom)

    return custom['person']['customId']


def get_fighter_custom_id(fighter_id):

    headers = get_headers()

    custom = get_endpoint_response(headers, f"fighter/get/{fighter_id}")

    return get_custom_id(custom['fighter']['personId'])

