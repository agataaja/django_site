import requests
import time


# Variáveis globais de cache
_cached_token = None
_token_expires_at = 0  # timestamp


def get_headers():

    api_key = 'jGpEm51R2k5nYZ6uVtcqjBnBsksrcUhteFfgFXPLhysSiW37he'
    client_id = 'b020a718926bba9cb4053adcb4cd22fc'
    client_secret = '89c383a23f21a3f0f33f8ddbe6194b89ec13cbe7e401416875cfdbea3740b3173178250509f28fe22bff23040232e2dd59c7041a907084aa1ecb15f0ddbb7153'
    ip = 'localhost'

    global _cached_token, _token_expires_at

    # Verifica se o token ainda está válido
    if _cached_token is None or time.time() >= _token_expires_at:
        _cached_token, _token_expires_at = get_token(ip, client_id, client_secret, api_key)
        print('new token')

    headers = {'Authorization': f'Bearer {_cached_token}'}

    return headers


def get_token(ip, client_id, client_secret, api_key):

    url = f'http://{ip}:8080/oauth/v2/token'
    params = {
        'grant_type': 'https://arena.uww.io/grants/api_key',
        'client_id': client_id,
        'client_secret': client_secret,
        'api_key': api_key
    }
    response = requests.post(url, params=params)
    data = response.json()

    print(data)

    access_token = data["access_token"]
    expires_in = data.get("expires_in", 3600)  # segundos
    expires_at = time.time() + expires_in - 60  # margem de 1 min

    return access_token, expires_at

