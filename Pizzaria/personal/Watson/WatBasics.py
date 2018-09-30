from __future__ import print_function
import json
from watson_developer_cloud import ConversationV1

from personal.firebase.DbBasic import DbBasic


class WatBasics:
    conversation = 0
    __workspace_id = 0
    __workspace = 0
    context = 0
    __respostas = ""
    __files = 0
    escritaValorPizza = {}
    escritaValorRefri = {}
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
        self.escritaValorPizza = {}
        self.escritaValorRefri = {}
        self.preco = 0
        self.originalEscritaRefri = {}
        self.originalEscritaPizza = {}
        self.cende = ""
        self.auxnum = {}

    def __getWorkspace(self):
        self.__workspace = self.conversation.get_workspace(workspace_id=self.__workspace_id, export=True)

    def __zerarContext(self):
        self.context = 0

    def fazerChamado(self, texto):
        self.files = open("analisador.txt", "a")
        if self.context == 0:
            self.__respostas = self.conversation.message(
                workspace_id=self.__workspace_id).result
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
            ).result
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
            "pizzas": self.escritaValorPizza,
            "refrigerante": self.escritaValorRefri,
            "observacao pedido": self.context['obspedido'],
            "nome": str(self.fire.pegarNome(self.context['telefone'])),
            "telefone": "".join(self.context['telefone'])
        }
        return pedido

    def calculaPreco(self):
        pizzas = self.fire.getPizzas()
        refris = self.fire.getRefri()
        som = 0
        for namep, names in self.originalEscritaPizza.items():
            som += int(self.escritaValorPizza[names]) * int(pizzas[namep]['preco'])
            print(som)
        for namep, names in self.originalEscritaRefri.items():
            som += int(self.escritaValorRefri[names]) * int(refris[namep]['preco'])
            print(str(som) + "refri")
        print(str(som))
        return som

    def linkarValores(self):
        tocheck = []
        checkpizza = False
        checkrefri = False
        auxpizza = {}
        auxrefri = {}
        dicRefri = {}
        dicPizza = {}
        self.auxnum = {}
        for entidade in self.__respostas['entities']:
            if entidade['entity'] == 'Sabores':
                auxpizza[entidade['value']] = self.__respostas['input']['text'][
                                              entidade['location'][0]:entidade['location'][1]]
                checkpizza = True
            if entidade['entity'] == 'Refrigerantes':
                auxrefri[entidade['value']] = self.__respostas['input']['text'][
                                              entidade['location'][0]:entidade['location'][1]]
                checkrefri = True
            if entidade['entity'] == 'sys-number':
                self.auxnum[entidade['value']] = self.__respostas['input']['text'][
                                                 entidade['location'][0]:entidade['location'][1]]
                tocheck.append(int(entidade['value']))
        if checkrefri or checkpizza:
            auxfrase = self.__respostas['input']['text'].split(" ")
            valp = list(auxpizza.values())
            valr = list(auxrefri.values())
            valnv = list(self.auxnum.values())
            valnk = list(self.auxnum.keys())
            # print(valp)
            # print(valr)
            for item in list(auxpizza.items()):
                self.originalEscritaPizza[item[0]] = item[1]
            for item in list(auxrefri.items()):
                self.originalEscritaRefri[item[0]] = item[1]
            while valp !=[]:
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
                        dicPizza[palavra] = valnk[valnv.index(var1)]
                        valnk.remove(valnk[valnv.index(var1)])
                        valnv.remove(var1)
                    elif var2 in valnv:
                        valp.remove(palavra)
                        dicPizza[palavra] = valnk[valnv.index(var2)]
                        valnk.remove(valnk[valnv.index(var2)])
                        valnv.remove(var2)
                    elif var3 in valnv:
                        valp.remove(palavra)
                        dicPizza[palavra] = valnk[valnv.index(var3)]
                        valnk.remove(valnk[valnv.index(var3)])
                        valnv.remove(var3)
                    else:
                        valp.remove(palavra)
                        dicPizza[palavra] = '1'
                        tocheck.append(1)
            while valr != []:
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
                        dicRefri[palavra] = valnk[valnv.index(var1)]
                        valnk.remove(valnk[valnv.index(var1)])
                        valnv.remove(var1)
                    elif var2 in valnv:
                        valr.remove(palavra)
                        dicRefri[palavra] = valnk[valnv.index(var3)]
                        valnk.remove(valnk[valnv.index(var3)])
                        valnv.remove(var3)
                    elif var3 in valnv:
                        valr.remove(palavra)
                        dicRefri[palavra] = valnk[valnv.index(var3)]
                        valnk.remove(valnk[valnv.index(var3)])
                        valnv.remove(var3)
                    else:
                        valr.remove(palavra)
                        dicRefri[palavra] = '1'

            if self.total == "":
                if sum(tocheck) > 1:
                    self.total += "então são"
                else:
                    self.total += "então é"
            lp = list(dicPizza.items())
            lr = list(dicRefri.items())

            for item in list(dicPizza.items()):
                self.escritaValorPizza[item[0]] = item[1]
            for item in list(dicRefri.items()):
                self.escritaValorRefri[item[0]] = item[1]

            for comp in lp:
                self.total += " " + str(comp[1]) + " " + comp[0]
                if lp.index(comp) == len(lp) - 1:
                    self.total += " e "
                else:
                    self.total += ","
            if dicRefri != {}:
                self.total += "junto com"

                for comp in lr:
                    self.total += " " + str(comp[1]) + " " + comp[0]
                    if lr.index(comp) == len(lr) - 1:
                        self.total += " e "
                    else:
                        self.total += ","

            self.context['frase'] = self.total
