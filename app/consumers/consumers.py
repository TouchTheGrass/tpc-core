
from channels.generic.websocket import WebsocketConsumer
import json
from channels.exceptions import DenyConnection
from django.contrib.auth.models import AnonymousUser
import datetime
from ..app.services.engine import EngineService
import time
from threading import Thread

from ..app.models.enumerations.player_status import PlayerStatus
from ..app.models.enumerations.piece_type import PieceType
from ..app.models.enumerations.piece_color import PieceColor
from ..app.models.enumerations.user_status import UserStatus
from ..app.models.enumerations.game_session_status import GameSessionStatus
from ..app.dto.piece_move import PieceMove
from ..app.dto.game_session import GameSession
from ..app.dto.ready_status import ReadyStatus
from ..app.dto.сolor import Color
from ..app.dto.connection import Connection
from ..app.dto.lobby_item import LobbyItem
from ..app.dto.piece_item import PieceItem
from ..app.dto.player_info_item import PlayerInfoItem
from ..app.dto.possible_moves_item import PossibleMovesItem
from ..app.dto.user_info_item import UserInfoItem
from ..app.dto.lobby_list import LobbyList
from ..app.dto.user_info_list import UserInfoList
from ..app.dto.player_info_list import PlayerInfoList
from ..app.dto.piece_list import PieceList
from ..app.dto.possible_moves_list import PossibleMovesList
from ..app.models.game_session import GameSessionModel
from ..app.models.user import UserModel
from ..app.models.user_game_session import UserGameSessionModel
from ..app.models.user_scores import UserScoresModel
from ..app.services.games import games
from ..app.services.games import GameInfo
from ..app.services.games import PlayerInfo
from ..app.services.games import Piece

class LobbyListWebsocket(WebsocketConsumer):

    def connect(self):
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")
        self.accept()

    def disconnect(self, code):
        pass


    def lobby_list(self):
        # отправка спичка свободных лобби
        self.send(text_data=json.dumps({
            'LobbyList': self.get_list_of_available_lobbies()
        }))

    def get_list_of_available_lobbies(self):
        # доступны лобби у которых game_session status -wait
        lobby_list = []
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
            lobby_list.append(lobby_item)
            lobby_list_obj=LobbyList(lobby_list)
        return lobby_list_obj
