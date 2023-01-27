from channels.generic.websocket import WebsocketConsumer
import json
from utils import get_list_of_available_lobbies
from channels.exceptions import DenyConnection
from django.contrib.auth.models import AnonymousUser
from ..app.models.enumerations.game_session_status import GameSessionStatus
from ..app.dto.lobby_item import LobbyItem

class LobbyList(WebsocketConsumer):

    def connect(self):
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")
        self.accept()

    def disconnect(self, code):
        pass

    def LobbyList(self):
        # отправка спичка свободных лобби
        self.send(text_data=json.dumps({
            'LobbyList': self.get_list_of_available_lobbies()
        }))

    def get_list_of_available_lobbies(self):
        # доступны лобби у которых game_session status -wait
        LobbyList = []
        waiting_game_sessions = GameSessionModel.objects.filter(status=GameSessionStatus("wait"))
        for el in waiting_game_sessions:
            # id игровой сессии
            game_session_id = el.id
            # получаем объекты участников конкретной сессии
            users = UserGameSessionModel.objects.filter(game_sessiion_id=el.id)
            # получим id игроков
            players_id = []
            for pl in users:
                players_id.append(pl.user_id)
            lobby_item=LobbyItem(game_session_id=game_session_id, players=players_id)
            LobbyList.append(lobby_item)
        return LobbyList
