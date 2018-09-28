import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import random


class DbBasic:

    def __init__(self):
        self.__cred = credentials.Certificate('/home/gutao/Desktop/mucha-pizza-firebase-adminsdk-lrard-794e3a2b61.json')
        self.__default_app = firebase_admin.initialize_app(self.__cred, {
            'databaseURL': 'https://mucha-pizza.firebaseio.com/'
        })
        self.id = random.randint(1, 1000)

    def pegarEndereco(self, numeroTelefone):
        aux = db.reference('users/' + "".join(numeroTelefone)).get()
        # print(aux)
        if aux is None:
            return None
        else:
            return aux['endereco']

    def pegarNome(self, numeroTelefone):
        aux = db.reference('users/' + "".join(numeroTelefone)).get()
        # print(aux)
        if aux is None:
            return None
        else:
            return aux['nome']

    def cadastrarUsuario(self, numero, endereco, nome):
        aux = db.reference('users')
        if numero in list(aux.get().keys()):
            aux.child("".join(numero)).update(
                {
                    'encereco': endereco,

                }
            )
        else:
            aux.child("".join(numero)).set(
                {
                    'endereco': endereco,
                    'nome': nome
                }
            )

    def gravarPedido(self, ped, num):
        # print("passei2")
        db.reference('pedidos').child(num).set(ped)
        self.id = random.randint(0, 1000)

    def getID(self):
        return self.id

    def getPizzas(self):
        return db.reference('pizzas').get()

    def getRefri(self):
        return db.reference('refrigerante').get()
