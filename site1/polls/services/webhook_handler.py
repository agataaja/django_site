from site1.polls.models import Luta
from site1.polls.integrations.api_arena import *
from site1.polls.utils.formatters import *
from site1.polls.integrations.sge_rest_api import *


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

    fights = get_fights_by_category("1f045f88-ae60-6e78-9005-6db8fc8b090d", categoria_id)

    for fight in fights:
        luta_obj = save_luta(fight, evento_id=143)
        sync_luta_with_remote(luta_obj)


def process_fight(data):
    luta_id = data.get("id")
    if not luta_id:
        return
    fight = get_fight(luta_id)
    luta_obj = save_luta(fight, evento_id=143)
    sync_luta_with_remote(luta_obj)


def process_event(data):
    sport_event_id = data.get("id")

    categeorias = get_weight_categories(sport_event_id)

    for id_categoria in categeorias.keys():

        fights = get_fights_by_category("1f045f88-ae60-6e78-9005-6db8fc8b090d", id_categoria)

        for fight in fights:
            luta_obj = save_luta(fight, evento_id=143)
            sync_luta_with_remote(luta_obj)


def save_luta(luta_data, evento_id):

    if luta_data.get("winnerFighterPersonId"):
        id_ganhador = get_fighter_custom_id(luta_data.get("winnerFighterPersonId"))
    else:
        id_ganhador = 0

    luta_obj, _ = Luta.objects.update_or_create(
        id=luta_data.get("id") + f"-{evento_id}",
        defaults={
            "id_evento": evento_id,
            "flag_finalizado": int(bool(luta_data.get("isCompleted", 0))),
            "round": luta_data.get("round", ""),
            "id_atleta_ganhador": id_ganhador,
            "sportAlternateName": luta_data.get("sportAlternateName", ""),
            "weightCategoryName": luta_data.get("weightCategoryName", ""),
            "audienceName": luta_data.get("audienceName", ""),
            "id_atleta1": get_custom_id(luta_data.get("fighter1PersonId")),
            "atleta1_flag_injured": int(bool(luta_data.get("fighter1IsInjured", 0))),
            "atleta1_flag_seeded": int(bool(luta_data.get("fighter1IsSeeded", 0))),
            "atleta1_draw_rank": luta_data.get("fighter1DrawRank", ""),
            "atleta1_RobinRank": luta_data.get("fighter1RobinRank", ""),
            "atleta1_ranking_point": luta_data.get("fighter1RankingPoint", 0),
            "id_atleta2": get_custom_id(luta_data.get("fighter2PersonId")),
            "atleta2_flag_injured": int(bool(luta_data.get("fighter2IsInjured", 0))),
            "atleta2_flag_seeded": int(bool(luta_data.get("fighter2IsSeeded", 0))),
            "atleta2_draw_rank": luta_data.get("fighter2DrawRank", ""),
            "atleta2_RobinRank": luta_data.get("fighter2RobinRank", ""),
            "atleta2_ranking_point": luta_data.get("fighter2RankingPoint", 0),
            "resultado": luta_data.get("result", ""),
            "tipo_vitoria": luta_data.get("victoryType", ""),
            "numero": luta_data.get("fightNumber", 0),
            "tapete": luta_data.get("matName", ""),
            "data_inicio": format_datetime(luta_data.get("expectedStartDate")),
            "data_fim": format_datetime(luta_data.get("completedDate")),
        },
    )
    return luta_obj
