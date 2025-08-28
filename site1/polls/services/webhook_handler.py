from ..models import Luta
from ..integrations.api_arena import *
from ..integrations.sge_rest_api import sync_luta_with_remote
from ..utils.id_request import get_customId_by_fighterId_or_return_0, get_customId_by_personId_or_return_0


def handle_webhook(data):

    entity = data.get("entity")

    if entity == "SportEventWeightCategory":
        process_category(data)

    elif entity == "Fight":
        process_fight(data)

    elif entity == "SportEvent":
        process_event(data)


def process_category(data):

    categoria_id = data.get("id")
    if not categoria_id:
        return

    category_info = get_weight_category_info_by_its_id(categoria_id)

    sport_event_id = category_info.get("sportEventId")

    fights = get_all_fights_by_event_id(sport_event_id)

    filtro = [item for item in fights if item.get("SportEventWeightCategoryId") == categoria_id]

    for fight in filtro:
        luta_obj = save_luta(fight, evento_id=143)
        # sync_luta_with_remote(luta_obj)


def process_fight(data):

    luta_id = data.get("id")
    if not luta_id:
        return
    fight = get_fight(luta_id)
    luta_obj = save_luta(fight, evento_id=14)
    # sync_luta_with_remote(luta_obj)


def process_event(data):
    print(">>> Iniciando process_event")

    start = time.perf_counter()

    sport_event_id = data.get("id")
    fights = get_all_fights_by_event_id(sport_event_id)

    for fight in fights:

        luta_obj = save_luta(fight, evento_id=140)
        # sync_luta_with_remote(luta_obj)

    end = time.perf_counter()
    elapsed = end - start

    print(f">>> Finalizou process_event, total de lutas do evento: {len(fights)}")
    print(f">>> Tempo de execução: {elapsed:.2f} segundos")


def save_luta(luta_data, evento_id):

    luta_obj, _ = Luta.objects.update_or_create(
        id=luta_data.get("id") + f"-{evento_id}",
        defaults={
            "id_evento": evento_id,
            "flag_finalizado": int(bool(luta_data.get("isCompleted", 0))),
            "round": luta_data.get("round", ""),
            "id_atleta_ganhador": get_customId_by_fighterId_or_return_0(luta_data.get("winnerFighter")),
            "sportAlternateName": luta_data.get("sportAlternateName", ""),
            "weightCategoryName": luta_data.get("weightCategoryName", ""),
            "audienceName": luta_data.get("audienceName", ""),

            "id_atleta1": get_customId_by_personId_or_return_0(luta_data.get("fighter1PersonId")),
            "atleta1_flag_injured": int(bool(luta_data.get("fighter1IsInjured", 0))),
            "atleta1_flag_seeded": int(bool(luta_data.get("fighter1IsSeeded", 0))),
            "atleta1_draw_rank": luta_data.get("fighter1DrawRank", ""),
            "atleta1_RobinRank": luta_data.get("fighter1RobinRank", ""),
            "atleta1_ranking_point": luta_data.get("fighter1RankingPoint", 0),

            "id_atleta2": get_customId_by_personId_or_return_0(luta_data.get("fighter2PersonId")),
            "atleta2_flag_injured": int(bool(luta_data.get("fighter2IsInjured", 0))),
            "atleta2_flag_seeded": int(bool(luta_data.get("fighter2IsSeeded", 0))),
            "atleta2_draw_rank": luta_data.get("fighter2DrawRank", ""),
            "atleta2_RobinRank": luta_data.get("fighter2RobinRank", ""),
            "atleta2_ranking_point": luta_data.get("fighter2RankingPoint", 0),
            "resultado": luta_data.get("result", ""),
            "tipo_vitoria": luta_data.get("victoryType", ""),
            "numero": luta_data.get("fightNumber", 0),
            "tapete": luta_data.get("matName", ""),
            "data_inicio": luta_data.get("expectedStartDate"),
            "data_fim": luta_data.get("completedDate"),
        },
    )
    return luta_obj
