from __future__ import print_function
import json
from watson_developer_cloud import ConversationV1

from firebase.DbBasic import DbBasic


class WatBaiscs:
    conversation = 0
    __workspace_id = 0
    __workspace = 0
    context = 0
    __respostas = ""
    __files = 0
    dicpizza = {}
    dicrefri = {}
    total = ""

    def __init__(self):
        self.conversation = ConversationV1(
            username='6ed890a0-5404-4920-bb55-a288f54041db',
            password='tSHLkaaci48t',
            ## url is optional, and defaults to the URL below. Use the correct URL for your region.
            url='https://gateway.watsonplatform.net/assistant/api',
            version='2018-09-11')

        self.__workspace_id = '16bf6f3b-466e-47cb-8228-49f9ec76eb6b'
        self.__getWorkspace()
        self.__zerarContext()
        self.fire = DbBasic()
        self.total = ""
        self.dicpizza = {}
        self.dicrefri = {}
        self.preco = 0
        self.auxrefri = {}
        self.auxpizza = {}
        self.cende = ""
        self.auxnum = {}
        self.fazerChamado('')

    def __getWorkspace(self):
        self.__workspace = self.conversation.get_workspace(workspace_id=self.__workspace_id, export=True)

    def __zerarContext(self):
        self.context = 0

    def fazerChamado(self, texto):
        self.files = open("analisador.txt", "a")
        if self.context == 0:
            self.__respostas = self.conversation.message(
                workspace_id=self.__workspace_id)
            self.context = self.__respostas['context']
            self.context['grava'] = "F"
            self.context['gravarende'] = "F"
            self.context['telefone'] = []
            self.context['ler'] = "F"
            self.context['pedido'] = 'Pedido' + str(self.fire.getID())
            self.context['obs'] = ''

        # elif self.context == finalnode:

        else:

            self.__respostas = self.conversation.message(
                workspace_id=self.__workspace_id, input={
                    'text': texto
                },
                context=self.context
            )
            self.context = self.__respostas['context']
        self.files.write(json.dumps(self.__respostas, indent=2))
        self.files.close()
        if len(self.__respostas['output']['text']) != 0:
            print("ela: " + ", ".join(self.__respostas['output']['text']))
        if self.context['gravarende'] == 'V':
            self.fire.cadastrarUsuario(self.context['telefone'], self.context['ende'], self.context['nome'])
            self.context['gravarende'] = 'F'

        self.linkarValores()
        # print(self.context['telefone'])
        self.buscarEndereco("".join(self.context['telefone']))
        # print(self.context['grava'])
        # print(self.context['ler'])
        # print(self.context['gravarende'])
        if self.context['grava'] == 'V':
            # print("passei1")
            self.fire.gravarPedido(self.montarPedido(), self.context['pedido'])
            self.context['grava'] = 'F'
            self.context = 0
        return ", ".join(self.__respostas['output']['text'])

    def adicionarContextVar(self, chave, valor):
        self.context[chave] = valor

    def buscarEndereco(self, telefone):
        if self.context['ler'] == "V":
            aju = self.fire.pegarEndereco(telefone)
            if aju is None:
                self.context['new'] = 'n'
                self.context['cende'] = 'Pelo visto você não tem cadastro'


            else:
                self.context['new'] = 's'
                self.context['cende'] = 'Bem vindo de novo ' + self.fire.pegarNome(self.context['telefone'])
                self.context['ende'] = aju
                self.total += 'entregar no endereço ' + aju + '?'
                self.context['frase'] = self.total

    def montarPedido(self):
        aux = self.context
        pedido = {
            "endereco": aux['ende'],
            "observacao pagamento": aux['obs'],
            "forma de pagamento": aux['fpag'],
            "preco": self.calculaPreco(),
            "status": "não atendido",
            "pizzas": self.dicpizza,
            "refrigerante": self.dicrefri,
            "observacao pedido": self.context['obspedido'],
            "nome": str(self.fire.pegarNome(self.context['telefone'])),
            "telefone": "".join(self.context['telefone'])
        }
        return pedido

    def calculaPreco(self):
        pizzas = self.fire.getPizzas()
        refris = self.fire.getRefri()
        som = 0
        for namep, names in self.auxpizza.items():
            som += int(self.dicpizza[names]) * int(pizzas[namep]['preco'])
            print(som)
        for namep, names in self.auxrefri.items():
            som += int(self.dicrefri[names]) * int(refris[namep]['preco'])
            print(som + "refri")
        print(som)
        return som


    def linkarValores(self):
        tocheck = []
        checkpizza = False
        checkrefri = False
        for entidade in self.__respostas['entities']:
            if entidade['entity'] == 'Sabores':
                self.auxpizza[entidade['value']] = self.__respostas['input']['text'][
                                                   entidade['location'][0]:entidade['location'][1]]
                checkpizza = True
            if entidade['entity'] == 'Refrigerantes':
                self.auxrefri[entidade['value']] = self.__respostas['input']['text'][
                                                   entidade['location'][0]:entidade['location'][1]]
                checkrefri = True
            if entidade['entity'] == 'sys-number':
                self.auxnum[entidade['value']] = self.__respostas['input']['text'][
                                            entidade['location'][0]:entidade['location'][1]]
                tocheck.append(int(entidade['value']))
        if checkrefri or checkpizza:
            auxfrase = self.__respostas['input']['text'].split(" ")
            self.dicpizza = {}
            self.dicrefri = {}
            valp = list(self.auxpizza.values())
            valr = list(self.auxrefri.values())
            valnv = list(self.auxnum.values())
            valnk = list(self.auxnum.keys())
            # print(valp)
            # print(valr)
            for palavra in valp:
                ind = auxfrase.index(palavra)
                var1 = ""
                var2 = ""
                var3 = ""
                if ind - 1 >= 0:
                    var1 = auxfrase[ind - 1]

                if ind - 2 >= 0:
                    var2 = auxfrase[ind - 2]

                if ind - 3 >= 0:
                    var3 = auxfrase[ind - 3]
                var1 = auxfrase[ind - 1]
                var2 = auxfrase[ind - 2]
                var3 = auxfrase[ind - 3]
                if var1 in valnv:
                    valp.remove(palavra)
                    self.dicpizza[palavra] = valnk[valnv.index(var1)]
                    valnk.remove(valnk[valnv.index(var1)])
                    valnv.remove(var1)
                elif var2 in valnv:
                    valp.remove(palavra)
                    self.dicpizza[palavra] = valnk[valnv.index(var2)]
                    valnk.remove(valnk[valnv.index(var2)])
                    valnv.remove(var2)
                elif var3 in valnv:
                    valp.remove(palavra)
                    self.dicpizza[palavra] = valnk[valnv.index(var3)]
                    valnk.remove(valnk[valnv.index(var3)])
                    valnv.remove(var3)
                else:
                    valp.remove(palavra)
                    self.dicpizza[palavra] = '1'
                    tocheck.append(1)

            for palavra in valr:
                ind = auxfrase.index(palavra)
                var1 = ""
                var2 = ""
                var3 = ""
                if ind - 1 >= 0:
                    var1 = auxfrase[ind - 1]

                if ind - 2 >= 0:
                    var2 = auxfrase[ind - 2]

                if ind - 3 >= 0:
                    var3 = auxfrase[ind - 3]

                if var1 in valnv:
                    valr.remove(palavra)
                    self.dicrefri[palavra] = valnk[valnv.index(var1)]
                    valnk.remove(valnk[valnv.index(var1)])
                    valnv.remove(var1)
                elif var2 in valnv:
                    valr.remove(palavra)
                    self.dicrefri[palavra] = valnk[valnv.index(var3)]
                    valnk.remove(valnk[valnv.index(var3)])
                    valnv.remove(var3)
                elif var3 in valnv:
                    valr.remove(palavra)
                    self.dicrefri[palavra] = valnk[valnv.index(var3)]
                    valnk.remove(valnk[valnv.index(var3)])
                    valnv.remove(var3)
                else:
                    valr.remove(palavra)
                    self.dicrefri[palavra] = '1'

            if self.total == "":
                if sum(tocheck) > 1:
                    self.total += "então são"
                else:
                    self.total += "então é"
            lp = list(self.dicpizza.items())
            lr = list(self.dicrefri.items())
            for comp in lp:
                self.total += " " + str(comp[1]) + " " + comp[0]
                if lp.index(comp) == len(lp) - 1:
                    self.total += " e "
                else:
                    self.total += ","
            if self.dicrefri != {}:
                self.total += "junto com"

                for comp in lr:
                    self.total += " " + str(comp[1]) + " " + comp[0]
                    if lr.index(comp) == len(lr) - 1:
                        self.total += " e "
                    else:
                        self.total += ","

            self.context['frase'] = self.total
