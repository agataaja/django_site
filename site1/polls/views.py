from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import WebhookPayload, Luta
from .services.webhook_handler import *


def index(request):

    # return HttpResponse("Olá esse é o meu primeiro site")
    return render(request, 'base.html')


def preview_view(request):

    return render(request, 'preview.html')


def pbi_view(request):

    return render(request, 'polls/pbi.html')


@csrf_exempt
def arena_receiver(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    WebhookPayload.objects.create(payload=data)
    handle_webhook(data)

    return JsonResponse({"status": "success", "message": "Webhook received"}, status=200)

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


