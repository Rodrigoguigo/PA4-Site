from __future__ import print_function
import json
from watson_developer_cloud import ConversationV1


class WatBaiscs:
    conversation = 0
    __workspace_id = 0
    __workspace = 0
    context = 0
    __respostas = ""
    __files = 0

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
        self.fazerChamado('')

    def __getWorkspace(self):
        self.__workspace = self.conversation.get_workspace(workspace_id=self.__workspace_id, export=True)

    def __zerarContext(self):
        self.context = 0

    def fazerChamado(self, texto):
        self.files = open("analisador.txt", "a")
        if self.context == 0:
            self.context = self.conversation.message(
                workspace_id=self.__workspace_id)

        # elif self.context == finalnode:

        else:

            self.context = self.conversation.message(
                workspace_id=self.__workspace_id, input={
                    'text': texto
                },
                context=self.context['context']
            )
        print(self.context)
        self.files.write(json.dumps(self.context, indent=2))
        self.files.close()
        print("ela: " + ", ".join(self.context['output']['text']))
        return ", ".join(self.context['output']['text'])
