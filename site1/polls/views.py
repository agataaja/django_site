from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import WebhookPayload, CredentialsArena, EventosArena, EventosSge, Luta
from .services.webhook_handler import handle_webhook
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CredentialsArenaForm
from.services.sge_handler import process_eventos_sge
from.services.arena_handler import fetch_eventos_arena
from django.contrib import messages


def sync_eventos_arena(request, pk):

    try:
        total = fetch_eventos_arena(pk)
        messages.success(request, f"{total} eventos sincronizados com sucesso!")
    except Exception as e:
        messages.error(request, f"Erro ao sincronizar: {str(e)}")

    return redirect("polls:eventos_arena_list", pk=pk)


def eventos_sge_list(request):

    eventos = EventosSge.objects.all()

    ano_filtro = request.GET.get('ano')
    escopo_filtro = request.GET.get('escopo')

    # Filtrar por ano se informado
    if ano_filtro:
        eventos = eventos.filter(ano=ano_filtro)

    # Filtrar por escopo se informado
    if escopo_filtro:
        eventos = eventos.filter(escopo=escopo_filtro)

    # Opções disponíveis para os filtros
    escopos = (
        EventosSge.objects.values_list('escopo', flat=True).distinct().order_by('escopo')
    )
    anos = (
        EventosSge.objects.values_list('ano', flat=True).distinct().order_by('-ano')
    )

    return render(request, 'eventos/sge_list.html', {
        'eventos': eventos,
        'anos': anos,
        'escopos': escopos
    })


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


def sync_eventos_sge(request):
    if request.method == "GET":
        process_eventos_sge()
        return redirect("polls:eventos_sge_list")

    else:
        return redirect("polls:eventos_sge_list")


def eventos_arena_list(request, pk):
    # Primeiro garante que a credencial existe
    credencial = get_object_or_404(CredentialsArena, pk=pk)

    # Pega todos os eventos associados a essa credencial
    eventos = EventosArena.objects.filter(credencial=credencial)

    return render(
        request,
        "eventos/arena_list.html",
        {
            "eventos": eventos,
            "credencial": credencial  # opcional, para exibir info da credencial na página
        }
    )

