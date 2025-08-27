import requests
from ..utils.formatters import format_datetime

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

    r = requests.get(f"{API_URL}?id={luta_obj.id}", headers=API_HEADERS)

    if r.status_code == 200:
        requests.put(f"{API_URL}/{luta_obj.id}", headers=API_HEADERS, json=payload)

    else:
        requests.post(API_URL, headers=API_HEADERS, json=payload)
