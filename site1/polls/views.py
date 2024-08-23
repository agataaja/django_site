from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):

    # return HttpResponse("Olá esse é o meu primeiro site")
    return render(request, 'base.html')


def doadores(request):

    return render(request, 'doadores.html')


def results():

    invalid = ''

    return invalid