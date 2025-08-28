import requests
from ..utils.formatters import format_datetime
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


API_URL = "https://restcbw.bigmidia.com/cbw/api/evento-luta"
API_HEADERS = {"Content-Type": "application/json"}


def sync_luta_with_remote(luta_obj):
    payload = {
        "id": luta_obj.id,
        "id_evento": luta_obj.id_evento,
        "numero": luta_obj.numero,
        "tapete": luta_obj.tapete,
        "round": luta_obj.round,
        "sportAlternateName": luta_obj.sportAlternateName,
        "weightCategoryName": luta_obj.weightCategoryName,
        "audienceName": luta_obj.audienceName,
        "id_classe_peso": luta_obj.id_classe_peso,
        "flag_finalizado": luta_obj.flag_finalizado,
        "id_atleta_ganhador": luta_obj.id_atleta_ganhador,
        "resultado": luta_obj.resultado,
        "tipo_vitoria": luta_obj.tipo_vitoria,
        "id_atleta1": luta_obj.id_atleta1,
        "atleta1_flag_injured": luta_obj.atleta1_flag_injured,
        "atleta1_flag_seeded": luta_obj.atleta1_flag_seeded,
        "atleta1_draw_rank": luta_obj.atleta1_draw_rank,
        "atleta1_RobinRank": luta_obj.atleta1_RobinRank,
        "atleta1_ranking_point": luta_obj.atleta1_ranking_point,
        "id_atleta2": luta_obj.id_atleta2,
        "atleta2_flag_injured": luta_obj.atleta2_flag_injured,
        "atleta2_flag_seeded": luta_obj.atleta2_flag_seeded,
        "atleta2_draw_rank": luta_obj.atleta2_draw_rank,
        "atleta2_RobinRank": luta_obj.atleta2_RobinRank,
        "atleta2_ranking_point": luta_obj.atleta2_ranking_point,
        "data_inicio": format_datetime(
            luta_obj.data_inicio),
        "data_fim": format_datetime(
            luta_obj.data_fim)
    }

    r = requests.get(f"{API_URL}/{luta_obj.id}", headers=API_HEADERS)

    if r.status_code == 200:

        print(f'Satus code atual da requisição de get {r}:', r.status_code)
        s = requests.put(f"{API_URL}/{luta_obj.id}", headers=API_HEADERS, json=payload)
        print('Satus code de envio do payload:', s.status_code, f'payload: {payload}')

    else:
        print(f'Satus code atual da requisição de {r}:', r.status_code)
        # p = requests.post(API_URL, headers=API_HEADERS, json=payload)
        p = requests.put(f"{API_URL}/{luta_obj.id}", headers=API_HEADERS, json=payload)
        print('Satus code de envio do payload:', p.status_code,f'status message: {p.text}', f'payload: {payload}')


def fetch_data(base_url, querys, headers, page):

    response = requests.get(f"{base_url}?{querys}page={page}", headers=headers).json()['items']
    return pd.json_normalize(response)


def clean_all_records():

    page_count = requests.get(f"{API_URL}", headers=API_HEADERS).json()["_meta"]["pageCount"]
    querys = f"&"

    print(page_count)

    with ThreadPoolExecutor() as executor:
        dfs = executor.map(lambda page: fetch_data(API_URL, querys, API_HEADERS, page), range(1, page_count + 1))

    final_df = pd.concat(dfs, ignore_index=True)

    for _, record in final_df.iterrows():

        id_luta = record['id']

        p = requests.delete(f'{API_URL}/{id_luta}')
        print(p.status_code, p.text)


def request_athlete_photo(id_atleta):

    url = f'https://restcbw.bigmidia.com/gestao/api/atleta/{id_atleta}'

    photo_id = requests.get(url, headers=API_HEADERS).json()['foto']

    photo_url = f'https://sge.cbw.org.br/_uploads/fotoAtleta/{photo_id}'

    return photo_url


def get_all_sge_eventos_info():

    headers = {"Content-Type": "application/json"}
    base_url = "https://restcbw.bigmidia.com/gestao/api/evento"
    querys = f"?flag_del=0&"

    page_count = requests.get(f"{base_url}{querys}", headers=headers).json()["_meta"]["pageCount"]

    with ThreadPoolExecutor() as executor:

        dfs = executor.map(lambda page: fetch_data(base_url, querys, headers, page), range(1, page_count+1))

    df = pd.concat(dfs, ignore_index=True)

    return df
