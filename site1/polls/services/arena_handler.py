from ..models import EventosArena, CredentialsArena
from ..integrations.api_arena import get_all_sport_events_info
from ..utils.maps import map_audience_name_by_name
from django.db import transaction


def fetch_eventos_arena(pk):

    eventos_api = get_all_sport_events_info(pk)['events']['items']
    objetos = []

    for item in eventos_api:
        objetos.append({
            "id_arena": item['id'],
            "nome_evento": item['name'],
            "isTeamEvent": item['isTeamEvent'],
            "isBeachWrestlingTournament": item['isBeachWrestlingTournament'],
            "audienceName": map_audience_name_by_name(item['name'])
        })

    credencial_obj = CredentialsArena.objects.get(pk=pk)  # ou pegue pelo id correto

    with transaction.atomic():
        for obj in objetos:
            EventosArena.objects.update_or_create(
                id_arena=obj['id_arena'],
                defaults={
                    "nome_evento": obj['nome_evento'],
                    "isTeamEvent": obj['isTeamEvent'],
                    "isBeachWrestlingTournament": obj['isBeachWrestlingTournament'],
                    "audienceName": obj['audienceName'],
                    "credencial": credencial_obj  # <-- isso é obrigatório
                }
            )