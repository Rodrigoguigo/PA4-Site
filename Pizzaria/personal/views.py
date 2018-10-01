from django.shortcuts import render, redirect
from django.http import HttpResponse
from .firebase.DbBasic import DbBasic
from .firebase.DbUser import DbUser
from .Watson.WatBasics import WatBasics
import json

WATSON = WatBasics()
DB = DbBasic()
USER = DbUser()

def index(request):
    global WATSON, DB
    WATSON = WatBasics()
    context = {
        'pizzas' : DB.getPizzas()
    }
    return render(request, 'personal/home.html', context)

def login(request):

    if 'email' not in request.POST:
        return render(request, 'personal/login.html')
  
    email = request.POST.get('email')
    password = request.POST.get('psw')

    USER.userLogin(email, password)

    if USER.isUserLoggedIn():
        return redirect('home')

    return render(request, 'personal/login.html', {'error':True})

def admin(request):
    global DB
    if not USER.isUserLoggedIn():
        return redirect('login')
    pedidos = DB.getPedidos()
    for chave, pedido in pedidos.items():
        if 'pizzas' in pedido:
            for chave_pizza in pedido['pizzas']:
                pedido['pizzas'][chave_pizza] = str(pedido['pizzas'][chave_pizza]) + " " + chave_pizza
        if 'refrigerante' in pedido:
            for chave_refri in pedido['refrigerante']:
                pedido['refrigerante'][chave_refri] = str(pedido['refrigerante'][chave_refri]) + " " + chave_refri

    context = {
        'pedidos' : pedidos
    }

    return render(request, 'personal/admin.html', context)

def adminCardapio(request):
    global DB
    if not USER.isUserLoggedIn():
        return redirect('login')
    context = {
        'pizzas':DB.getPizzas()
    }
    return render(request, 'personal/admincardapio.html', context)

def addPizza(request):
    if USER.isUserLoggedIn():
        context = {}

        if 'nome'in request.POST:
            values = {
                'nome':request.POST['nome'],
                'descricao':request.POST['desc'],
                'imagem':request.POST['img'],
                'preco':request.POST['preco']
            }
           
            context = {'result':USER.createPizza(values['nome'], values)}
       
        return render(request, 'personal/add.html', context)

    return redirect('login')

def sendMessage(request):
    message = request.POST.get('message')
    data = {
        'response' : WATSON.fazerChamado(message)
    }
    return HttpResponse(json.dumps(data), content_type='application/json')
