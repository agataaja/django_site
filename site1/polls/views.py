from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import WebhookPayload, Luta
from .authorization_arena import get_headers
import requests
from .api_arena import get_custom_id, get_fighter_custom_id


def index(request):

    # return HttpResponse("Olá esse é o meu primeiro site")
    return render(request, 'base.html')


def preview_view(request):

    return render(request, 'preview.html')


def pbi_view(request):

    return render(request, 'polls/pbi.html')


@csrf_exempt
def arena_receiver(request):

    if request:
        try:
            data = json.loads(request.body)
            WebhookPayload.objects.create(payload=data)
            print("Received webhook payload:", data)

            if data.get('entity') == 'SportEventWeightCategory':

                categoria_id = data.get('id')
                if not categoria_id:
                    return JsonResponse({'error': 'ID da categoria não encontrado'}, status=400)

                headers = get_headers()
                session = requests.Session()

                url = f'http://localhost:8080/api/json/fight/1f01af00-0d57-6d1e-9360-55c001b924eb/bracket/{categoria_id}'
                response = session.get(url, headers=headers)

                if response.status_code != 200:
                    return JsonResponse({'error': 'Erro ao buscar lutas da API'}, status=500)

                dados = response.json()

                for luta_data in dados.get('fights', []):

                    luta_id = luta_data.get('id')

                    if not luta_id:
                        continue

                    # Atualiza ou cria
                    Luta.objects.update_or_create(
                        id=luta_id,
                        defaults={
                            'id_evento': 143,
                            'id_atleta1': get_custom_id(luta_data.get('fighter1PersonId')),
                            'id_atleta2': get_custom_id(luta_data.get('fighter2PersonId')),
                            'flag_finalizado': luta_data.get('isCompleted', 0),
                            'round': luta_data.get('round', ''),
                            'id_atleta_ganhador': get_fighter_custom_id(luta_data.get('winnerFighter')),
                            'sportAlternateName': luta_data.get('sportAlternateName', ''),
                            'weightCategoryName': luta_data.get('weightCategoryName', ''),
                            'audienceName': luta_data.get('audienceName', ''),
                            'atleta1_flag_injured': luta_data.get('fighter1IsInjured', 0),
                            'atleta1_flag_seeded': luta_data.get('fighter1IsSeeded', 0),
                            'atleta1_draw_rank': luta_data.get('fighter1DrawRank', ''),
                            'atleta1_RobinRank': luta_data.get('fighter1RobinRank', ''),
                            'atleta2_flag_injured': luta_data.get('fighter2IsInjured', 0),
                            'atleta2_flag_seeded': luta_data.get('fighter2IsSeeded', 0),
                            'atleta2_draw_rank': luta_data.get('fighter2DrawRank', ''),
                            'atleta2_RobinRank': luta_data.get('fighter2RobinRank', ''),
                            'resultado': luta_data.get('result', ''),
                            'tipo_vitoria': luta_data.get('victoryType', ''),
                            'atleta1_ranking_point': luta_data.get('fighter1RankingPoint', 0),
                            'atleta2_ranking_point': luta_data.get('fighter2RankingPoint', 0),
                            'numero': luta_data.get('fightNumber', 0),
                            'tapete': luta_data.get('matName', ''),
                            'data_inicio': luta_data.get('startDate'),
                            'data_fim': luta_data.get('completedDate'),
                        }
                    )

            elif data.get('entity') == 'Fight': # or data.get('entity') == 'FightRankingPoint':
                fight_id = data.get('id')

                if not fight_id:
                    return JsonResponse({'error': 'ID da luta não encontrado'}, status=400)

                headers = get_headers()
                session = requests.Session()

                url = f'http://localhost:8080/api/json/fight/get/{fight_id}'
                response = session.get(url, headers=headers)

                if response.status_code != 200:
                    return JsonResponse({'error': 'Erro ao buscar lutas da API'}, status=500)

                dados = response.json()

                fight = dados.get('fight', {})

                if fight.get('winnerFighterPersonId'):

                    id_ganhador = get_custom_id(fight.get('winnerFighterPersonId'))

                else:

                    id_ganhador = 0

                # Atualiza ou cria
                Luta.objects.update_or_create(

                    id=fight_id,
                    defaults={
                        'id_evento': 143,
                        'id_atleta1': get_custom_id(fight.get('fighter1PersonId')),
                        'id_atleta2': get_custom_id(fight.get('fighter2PersonId')),
                        'flag_finalizado': fight.get('isCompleted', 0),
                        'round': fight.get('round', ''),
                        'id_atleta_ganhador': id_ganhador,
                        'sportAlternateName': fight.get('sportAlternateName', ''),
                        'weightCategoryName': fight.get('weightCategoryName', ''),
                        'audienceName': fight.get('audienceName', ''),
                        'atleta1_flag_injured': fight.get('fighter1IsInjured', 0),
                        'atleta1_flag_seeded': fight.get('fighter1IsSeeded', 0),
                        'atleta1_draw_rank': fight.get('fighter1DrawRank', ''),
                        'atleta1_RobinRank': fight.get('fighter1RobinRank', ''),
                        'atleta2_flag_injured': fight.get('fighter2IsInjured', 0),
                        'atleta2_flag_seeded': fight.get('fighter2IsSeeded', 0),
                        'atleta2_draw_rank': fight.get('fighter2DrawRank', ''),
                        'atleta2_RobinRank': fight.get('fighter2RobinRank', ''),
                        'resultado': fight.get('result', ''),
                        'tipo_vitoria': fight.get('victoryType', ''),
                        'atleta1_ranking_point': fight.get('fighter1RankingPoint', 0),
                        'atleta2_ranking_point': fight.get('fighter2RankingPoint', 0),
                        'numero': fight.get('fightNumber', 0),
                        'tapete': fight.get('matName', ''),
                        'data_inicio': fight.get('expectedStartDate'),
                        'data_fim': fight.get('completedDate'),
                    }
                )

            return JsonResponse({'status': 'success', 'message': 'Webhook received successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


def arena_show(request):

    lutas_json(request)

    return render(request, 'polls/arena-web-hooking-show.html')


def lutas_json(request):

    lutas = list(Luta.objects.values())
    return JsonResponse({'lutas': lutas})


def results():

    invalid = ''

    return invalid


def chaveamento_view(request, id_evento):
    lutas = (
        Luta.objects
        .filter(id_evento=id_evento)
        .order_by('round', 'numero')  # organiza as lutas por fase e ordem
    )

    # estrutura tipo {"Quartas de Final": [luta1, luta2], "Semifinal": [...], "Final": [...]}
    chaveamento = {}
    for luta in lutas:
        chaveamento.setdefault(luta.round, []).append(luta)

    return render(request, "polls/chaveamento.html", {"chaveamento": chaveamento})


