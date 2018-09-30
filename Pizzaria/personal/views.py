from django.shortcuts import render
from django.http import HttpResponse
from .firebase.DbBasic import DbBasic
from .Watson.WatBasics import WatBasics
import json

WATSON = WatBasics()
DB = DbBasic()

def index(request):
    global WATSON, DB
    WATSON = WatBasics()
    context = {
        'pizzas' : DB.getPizzas()
    }
    return render(request, 'personal/home.html', context)

def login(request):
    return render(request, 'personal/login.html')

def admin(request):
    return render(request, 'personal/admin.html')

def adminCardapio(request):
    return render(request, 'personal/admincardapio.html')

def addPizza(request):
    return render(request, 'personal/add.html')

def sendMessage(request):
    message = request.POST.get('message')
    data = {
        'response' : WATSON.fazerChamado(message)
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
