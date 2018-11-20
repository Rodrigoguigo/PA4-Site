from django.shortcuts import render, redirect
from django.http import HttpResponse
from .firebase.DbBasic import DbBasic
from .firebase.DbUser import DbUser
from .Watson.WatBasics import WatBasics
from datetime import datetime
import json

WATSON = WatBasics()
DB = DbBasic()
USER = DbUser()

def index(request):
    global WATSON, DB
    WATSON.reiniciarConversa();
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
    global DB, USER
    if not USER.isUserLoggedIn():
        return redirect('login')
    pedidos = DB.getPedidos()

    if pedidos is not None:
        for chave, pedido in pedidos.items():
            if 'pizzas' in pedido:
                for chave_pizza in pedido['pizzas']:
                    pedido['pizzas'][chave_pizza] = str(pedido['pizzas'][chave_pizza]) + " " + chave_pizza
            if 'refrigerante' in pedido:
                for chave_refri in pedido['refrigerante']:
                    pedido['refrigerante'][chave_refri] = str(pedido['refrigerante'][chave_refri]) + " " + chave_refri
            pedido['data_pedido'] = datetime.strptime(pedido['data_pedido'], '%Y-%m-%d %H:%M:%S.%f')
   
        pedidos = sorted(pedidos.items(), key=lambda x: (x[1]['data_pedido'], x[0]), reverse=True)

    context = {
        'pedidos' : pedidos
    }

    return render(request, 'personal/admin.html', context)

def adminCardapio(request):
    global DB, USER
    if not USER.isUserLoggedIn():
        return redirect('login')

    if 'remove' in request.POST:
        USER.deletePizza(request.POST['remove'])
    elif 'edit' in request.POST:
        USER.updatePizza(request.POST['edit'], {
            'nome':request.POST['edit'],
            'imagem':request.POST['img'],
            'descricao':request.POST['desc'],
            'preco':request.POST['preco']
        })

    context = {
        'pizzas':DB.getPizzas()
    }

    return render(request, 'personal/admincardapio.html', context)

def addPizza(request):
    global USER
    if USER.isUserLoggedIn():
        context = {}

        if 'nome' in request.POST:
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

def completeOrder(request):
    global USER

    pedido = request.POST['pedido']

    USER.deletePedido(pedido)

    return checkUpdates(request)

def getListaPedidos(request):
    global DB

    pedidos = DB.getPedidos()

    if pedidos is not None:
        for chave, pedido in pedidos.items():
            if 'pizzas' in pedido:
                for chave_pizza in pedido['pizzas']:
                    pedido['pizzas'][chave_pizza] = str(pedido['pizzas'][chave_pizza]) + " " + chave_pizza
            if 'refrigerante' in pedido:
                for chave_refri in pedido['refrigerante']:
                    pedido['refrigerante'][chave_refri] = str(pedido['refrigerante'][chave_refri]) + " " + chave_refri
            pedido['data_pedido'] = datetime.strptime(pedido['data_pedido'], '%Y-%m-%d %H:%M:%S.%f')
   
        pedidos = sorted(pedidos.items(), key=lambda x: (x[1]['data_pedido'], x[0]), reverse=True)

    context = {
        'pedidos' : pedidos
    }

    return render(request, 'personal/listaPedidosAdmin.html', context)

def getPedido(request, fone):
    global DB

    pedido = DB.getPedido(fone)

    context = {
        'pedido' : pedido
    }

    if not pedido:
        print(pedido)
        return render(request, 'personal/semPedido.html')
    else:
        return render(request, 'personal/pedidoInfo.html', context)

def getListaPizzas(request):
    global DB

    pizzas = DB.getPizzas()

    context = {
            'pizzas' : pizzas
    }

    return render(request, 'personal/listaPizzas.html', context)

def checkUpdates(request):
    global DB
    context = ''

    if 'pedidos' in request.POST['message']:
        pedidos = DB.getPedidos()

        if pedidos is not None:
            for chave, pedido in pedidos.items():
                if 'pizzas' in pedido:
                    for chave_pizza in pedido['pizzas']:
                        pedido['pizzas'][chave_pizza] = str(pedido['pizzas'][chave_pizza]) + " " + chave_pizza
                    pedido['pizzas'] = ', '.join(x for x in pedido['pizzas'].values())
                if 'refrigerante' in pedido:
                    for chave_refri in pedido['refrigerante']:
                        pedido['refrigerante'][chave_refri] = str(pedido['refrigerante'][chave_refri]) + " " + chave_refri
                    pedido['refrigerante'] = ', '.join(x for x in pedido['refrigerante'].values())
                pedido['data_pedido'] = datetime.strptime(pedido['data_pedido'], '%Y-%m-%d %H:%M:%S.%f')

            pedidos = sorted(pedidos.items(), key=lambda x: (x[1]['data_pedido'], x[0]), reverse=True)

        context = {
            'pedidos' : pedidos
        }
    elif 'pizzas' in request.POST['message']:
        pizzas = DB.getPizzas()
        context = {
            'pizzas' : pizzas
        }

    return HttpResponse(json.dumps(context, default=str), content_type='application/json')
