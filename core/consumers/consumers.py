from channels.generic.websocket import WebsocketConsumer
import json
from utils import get_list_of_available_lobbies
from channels.exceptions import DenyConnection
from django.contrib.auth.models import AnonymousUser

class LobbyList(WebsocketConsumer):

    def connect(self):
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")
        self.accept()

    def disconnect(self, code):
        pass

    def list_of_available_lobbies(self):
        # отправка спичка свободных лобби
        self.send(text_data=json.dumps({
            'list_of_available_lobbies': get_list_of_available_lobbies()
        }))
