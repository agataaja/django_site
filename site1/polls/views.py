from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import WebhookPayload, CredentialsArena, EventosArena, EventosSge, Luta
from .services.webhook_handler import handle_webhook
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CredentialsArenaForm
from.services.sge_handler import process_eventos


def eventos_sge_list(request):
    eventos = EventosSge.objects.all()
    return render(request, 'eventos/sge_list.html', {'eventos': eventos})


def index(request):
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
        print('webhook recebido', data)
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


# Listagem
def credentials_list(request):
    creds = CredentialsArena.objects.all()
    return render(request, "polls/credentials/list.html", {"creds": creds})


# Cadastro
def credentials_create(request):
    if request.method == "POST":
        form = CredentialsArenaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("polls:credentials_list")
    else:
        form = CredentialsArenaForm()
    return render(request, "polls/credentials/form.html", {"form": form})


# Edição
def credentials_edit(request, pk):
    cred = get_object_or_404(CredentialsArena, pk=pk)
    if request.method == "POST":
        form = CredentialsArenaForm(request.POST, instance=cred)
        if form.is_valid():
            form.save()
            return redirect("polls:credentials_list")
    else:
        form = CredentialsArenaForm(instance=cred)
    return render(request, "polls/credentials/form.html", {"form": form})


# Exclusão
def credentials_delete(request, pk):
    cred = get_object_or_404(CredentialsArena, pk=pk)
    if request.method == "POST":
        cred.delete()
        return redirect("polls:credentials_list")
    return render(request, "polls/credentials/confirm_delete.html", {"cred": cred})


def eventos_sge_upload(request):
    if request.method == "GET":
        process_eventos()
        return redirect("polls:eventos_arena_list")

    else:
        return redirect("polls:eventos_arena_list")



