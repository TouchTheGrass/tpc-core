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



class Interaction_With_The_Lobby(WebsocketConsumer):
    # соединение хранит id соединенного пользователя и id ранее упомянутой game_session
    # при успешном соединении user_game_session.status = not_ready
    def connect(self):
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")
        self.accept()

    def disconnect(self, content):
        user_id = content["user_id"]
        user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id = user_game_session[0].game_session_id

        # если пользователь имеет активную user_game_session и game_session.status == wait
        if user_game_session.exists()==True and\
            GameSessionModel.objects.get(id=session_id).status == GameSessionStatus("wait"):
                user_game_session.delete()
        # если пользователь имеет активную user_game_session и game_session.status == game
        if user_game_session.exists() == True and \
                GameSessionModel.objects.get(id=session_id).status == GameSessionStatus("game"):
                    user_game_session[0].status=UserStatus("disconnected")
                    # если активная user_game_session имеет статус disconnected более 60 секунд
                    # таймер запускается в отдельном потоке
                    game_end = Thread(target=self.game_end_timer)
                    game_end.start()

    def receive(self, text_data):
        comand=json.loads(text_data)
        user_id=self.scope["user"]
        if comand.get("type")=='request':
            if comand.get("value")=="create_lobby":
                self.create_lobby(user_id)
            elif comand.get("value")=="consider":
                self.consider(user_id)

        elif comand.get("type")=="connect_lobby":
            session_id=comand.get("session_id")
            self.connect_lobby(user_id, session_id)

        elif comand.get("type")=="change_color":
            color=comand.get("color")
            self.change_color(user_id, color)

        elif comand.get("type")=="change_readiness":
            user_status=comand.get("status")
            self.change_readiness(user_id, user_status)

        elif comand.get("type")=="move_piece":
            piece_id=comand.get("piece_id")
            position=comand.get("position")
            self.move_piece(user_id, piece_id, position)

        elif comand.get("type")=="game_session":
            self.return_game_session_info(user_id)

        elif comand.get("type")=="user_info_list":
            self.return_user_info_list(user_id)

        elif comand.get("type")=="player_info_list":
            self.return_player_info_list(user_id)

        elif comand.get("type")=="piece_list":
            self.retur_piece_list(user_id)

        elif comand.get("type")=="possible_moves_list":
            self.possible_moves_list(user_id)


    # ________________________________________________________________________________
    # Подключенным пользователям требуется предоставлять следующие данные
    #________________________________________________________________________________
    # Предоставление информации об активной game_session
    def return_game_session_info(self, content):
        user_id=content["user_id"]
        user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists()==False:
            self.send(text_data=json.dumps({
                'GameSession': None
            }))
        # у пользователя есть уникальная запись user_game_session -> отправляется информация об активной game_session
        # обновление должно происходить при изменении статуса игровой сессии
        else:
            game_id=user_game_session[0].game_session_id
            game_session_obj=GameSessionModel.objects.get(id=game_id)
            self.send(text_data=json.dumps({
                'GameSession':GameSession(id=game_session_obj.id, status=game_session_obj.status)
            }))

    # Предоставление списка user_gamer_session, ссылающихся на активную game_session
    # обновление должно происходить при изменении информации о пользователей текущей сессии:
    # при добавлении/удалении пользователя
    # при изменении статуса пользователя
    # при изменении цвета пользователем
    def return_user_info_list(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'UserInfoList': None
            }))
        else:
            game_id = user_game_session[0].game_session_id
            user_list=UserGameSessionModel.objects.filter(game_session_id=game_id)
            user_info_list=[]
            for obj in user_list:
                user_name=UserModel.objects.get(id=obj.user_id).name
                user_info_list.append(UserInfoItem(id=obj.id, name=user_name, status=obj.status, color=obj.color))

            self.send(text_data=json.dumps({
                'UserInfoList': UserInfoList(user_info_list)
            }))

    # Предоставление списка player_info
    # обновляется в случае изменения внутриигрового статуса
    def return_player_info_list(self, content):
        user_id=content["user_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'PlayerInfoList': None
            }))
        else:
            game_id=user_game_session[0].game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSessionModel.objects.filter(id=game_id, status=GameSessionStatus("game")).exists()==False:
                self.send(text_data=json.dumps({
                    'PlayerInfoList': None
                }))
            else:
                # у пользователя есть активная user_game_session, у которой status == game
                player_info_list=[]

                player_list = games[game_id].players

                for obj in player_list:
                    player_info_list.append(PlayerInfoItem(id=obj.user_id,status=obj.status))

                self.send(text_data=json.dumps({
                    'PlayerInfoList': PlayerInfoList(player_info_list)
                }))

    # Предоставление списка piece
    # обновляется при изменении данных фигуры:
    # тип
    # позиция
    # цвет
    def retur_piece_list(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'PieceList': None
            }))
        else:
            game_id = user_game_session[0].game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSessionModel.objects.filter(id=game_id, status=GameSessionStatus("game")).exists() == False:
                self.send(text_data=json.dumps({
                    'PieceList': None
                }))
            else:
                # у пользователя есть активная user_game_session, у которой status == game
                obj_piece_list=[]

                piece_list = games[game_id].pieces

                for obj in piece_list:
                    obj_piece_list.append(PieceItem(id=obj.id,type=obj.type,color=obj.color,position=obj.position))


                self.send(text_data=json.dumps({
                    'PieceList': PieceList(obj_piece_list)
                }))

    # Предоставление списка доступных ходов
    # обновляется после каждого хода
    def possible_moves_list(self, content):
        user_id=content["user_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        # цвет за который играет пользователь
        color_value=user_game_session[0].color.value
        session_id=user_game_session[0].game_session_id

        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'PossibleMovesList': None
            }))
        else:
            game_id = user_game_session[0].game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSessionModel.objects.filter(id=game_id, status=GameSessionStatus("game")).exists() == False:
                self.send(text_data=json.dumps({
                    'PossibleMovesList': None
                }))
            else:
                # у пользователя есть активная user_game_session, у которой status == game
                possible_moves_list=[]
                our_pieces_id=[]
                # получаем все фигуры пользователя
                # получаем список ВСЕХ фигур данной игровой сессии
                all_pieces=games[session_id].pieces
                # obj - объект Piece
                for obj in all_pieces:
                    # добавляем id фигур нашего цвета в список
                    if obj.color.value==color_value:
                        our_pieces_id.append(id(obj))

                for piece_id in our_pieces_id:
                    available_move_list=EngineService.get_possible_moves(session_id, piece_id)
                    possible_moves_item=PossibleMovesItem(piece_id=piece_id, possible_moves=available_move_list)
                    possible_moves_list.append(possible_moves_item)


                self.send(text_data=json.dumps({
                    'PossibleMovesList': PossibleMovesList(possible_moves_list)
                }))

    # ________________________________________________________________________________
    # от подключенных требуется обрабатывать следующие запросы:
    # ________________________________________________________________________________

    # запрос на присоединение к лобби
    def connect_lobby(self, content ):
        user_id=content["user_id"]
        session_id=content["session_id"]
        if GameSessionModel.objects.get(id=session_id).status==GameSessionStatus("wait"):
            # если нет активных game_session у инициализатора и
            # связанных с game_session user_game_session менее 3
            if UserGameSessionModel.objects.filter(user_id=user_id, active=True).exists()==False and\
                len(UserGameSessionModel.objects.filter(game_session_id=session_id))<3:
                    user_game_session = UserGameSessionModel(
                        user_id=user_id,
                        game_session_id=session_id,
                        active=True,
                        status=UserStatus("not_ready"),
                        color=None,
                        is_winner=None,
                        scores=None,
                        created_at=datetime.datetime.now(),
                        updated_at=datetime.datetime.now()
                    )
                    user_game_session.save()

            self.send(text_data=json.dumps({
                'Connection': Connection(game_session_id=session_id)
            }))
        # если у подключаемой game_session status == game
        if GameSessionModel.objects.get(id=session_id).status==GameSessionStatus("game"):
            # требуется наличие активной game_session у инициализатора
            if UserGameSessionModel.objects.filter(user_id=user_id, game_session_id=session_id,active=True).exists() == True:
                user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, game_session_id=session_id,active=True)
                user_game_session[0].status=UserStatus("playing")

                self.send(text_data=json.dumps({
                    'Connection': Connection(game_session_id=session_id)
                }))
        # обновление при изменении статуса игровой сессии
        self.return_game_session_info(user_id)
        # обновление при добавлении/удалении пользователя
        self.return_user_info_list(user_id)


    # запрос на создание лобби
    def create_lobby(self, content):
        user_id=content["user_id"]
        # отсутствие активной game_session у инициализатора
        if UserGameSessionModel.objects.filter(user_id=user_id, active=True).exists() == False:
            game_session=GameSessionModel(
                status=GameSessionStatus("wait")
            )
            game_session.save()
            session_id=game_session.id
            # создание объектов фигур и их расстановка
            pieces_list=self.piece_generation(session_id)

            games[session_id]=\
                GameInfo(\
                        players=[PlayerInfo(user_id=user_id, game_session_id=session_id, status=PlayerStatus("wait_turn"))],\
                        pieces=[pieces_list])

            user_game_session = UserGameSessionModel(
                user_id=user_id,
                game_session_id=session_id,
                active=True,
                status=UserStatus("not_ready"),
                color=None,
                is_winner=None,
                scores=None,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now()
            )
            user_game_session.save()
        # обновление при добавлении/удалении пользователя
        self.return_user_info_list(user_id)


    # смена цвета фигур для текущего пользователя
    def change_color(self, content):
        user_id = content["user_id"]
        # color - строка например "white"
        color=PieceColor(content["color"])
        # требуется активная user_gamer_session у пользователя
        user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id=user_game_session[0].game_session_id
        if user_game_session.exists() == True:
            # получаем доступные цвета
            user_gamer_session = UserGameSessionModel.objects.filter(game_session_id=session_id)
            for obj in user_gamer_session:
                if obj.color == color:
                    # Такой цвет нельзя выбрать
                    self.send(text_data=json.dumps({
                        'Color': None
                    }))
            user_game_session[0].color=color
            self.send(text_data=json.dumps({
                'Color': Color(value=color)
            }))
        # обновление при изменении цвета пользователем
        self.return_user_info_list(content)

    # смена статуса о готовности для текущего пользователя
    def change_readiness(self, content):
        user_id = content["user_id"]
        # user_status - объект типа ReadyStatus
        user_status=content["status"]
        # требуется активная user_gamer_session у пользователя
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id=user_game_session[0].game_session_id
        if user_game_session.exists() == True:
            user_game_session[0].status=UserStatus(user_status)
        self.send(text_data=json.dumps({
            'ReadyStatus': ReadyStatus(value=user_status)
        }))

        # проверка и изменение статуса game_session на game
        self.changing_game_status_to_game(session_id)
        # обновление при изменении статуса игровой сессии
        self.return_game_session_info(content)
        # обновление при изменении статуса пользователя
        self.return_user_info_list(content)

    # запрос на передвижение фигуры
    def move_piece(self, content):
        user_id = content["user_id"]
        piece_id=content["piece_id"]
        position=content["position"]
        user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id = user_game_session[0].game_session_id
        # если есть активная user_game_session у пользователя и game_session.status == game
        if user_game_session.exists() == True and GameSessionModel.objects.filter(id=session_id, status=GameSessionStatus("game")).exists()==True:
            # требуется player_info.status == current_turn
            list_player_info=games[session_id].players
            # obj- объект PlayerInfo
            for obj in list_player_info:
                # находим текущего пользователя
                if obj.user_id==user_id:
                    if obj.player_status==PlayerStatus("current_turn"):
                        # параметры связанных piece меняются в соответствии с правилами
                        EngineService.move_piece(session_id,piece_id,position)
                        #параметры player_info меняются в соответствии с правилами

            self.send(text_data=json.dumps({
                'PieceMove': PieceMove(id=piece_id, position=position)
            }))

            # обновляется в случае изменения внутриигрового статуса
            self.return_player_info_list(content)
            # обновляется при изменении данных фигуры
            self.retur_piece_list(content)
            # обновляется после каждого хода
            self.possible_moves_list(content)

    # запрос сдаться
    def consider(self, content):
        user_id=content["user_id"]
        # требуется активная user_game_session у пользователя и
        # требуется user_game_session.status == game
        user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, active=True, status=UserStatus("playing"))
        session_id=user_game_session[0].game_session_id
        cur_color=user_game_session[0].color
        if user_game_session.exists() == True:
            # игра заканчивается
            game_session=GameSessionModel.objects.get(id=session_id)
            game_session.status=GameSessionStatus("completed")
            # обновление при изменении статуса игровой сессии
            self.return_game_session_info(user_id)
            # user_game_session у игроков данной сессии становятся неактивными
            user_game_session=UserGameSessionModel.objects.filter(game_session_id=session_id)
            # находим у кого максимальное колиечество баллов и не сдался- победитель
            max_score=0

            for obj in user_game_session:
                if obj.scores>max_score:
                    max_score=obj.scores
                    color_winner=obj.color

            for obj in user_game_session:
                obj.active=False
                obj.status=UserStatus("disconnected")
                # максимальное число баллов и игрок не сдался
                if obj.color==color_winner and obj.color!=cur_color:
                    obj.is_winner = True
                else:
                    obj.is_winner=False
                # начисление очков
                scores=int(obj.scores)
                score_table=UserScoresModel.objects.get(user_id=user_id)
                score_table.scores+=scores
        # обновление при изменении статуса пользователя
        self.return_user_info_list(user_id)

    # вспомогательный метод на изменение статуса игры на game с контролем условий:
    # существует 3 user_game_session связанных с game_session
    # все user_game_session связанные с game_session имеют статус ready
    # game_session.status == wait
    def changing_game_status_to_game(self, game_session_id):
        game_session_obj=GameSessionModel.objects.get(id=game_session_id)
        user_game_session_list=UserGameSessionModel.objects.filter(game_session_id=game_session_id)
        if game_session_obj.status==GameSessionStatus("wait") and\
            len(user_game_session_list)==3:
                for obj in user_game_session_list:
                    if obj.status!=UserStatus("ready"):
                        return 0
                game_session_obj.status=GameSessionStatus("game")

    def game_end_timer(self, content):
        user_id = content["user_id"]
        time.sleep(60)
        # если активная user_game_session имеет статус disconnected, игра заканчивается
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id=user_game_session[0].game_session_id
        cur_color = user_game_session[0].color
        if user_game_session[0].status==UserStatus("disconnected"):
            # игра заканчивается
            game_session = GameSessionModel.objects.get(id=session_id)
            game_session.status = GameSessionStatus("completed")
            # обновление при изменении статуса игровой сессии
            self.return_game_session_info(content)
            # user_game_session у игроков данной сессии становятся неактивными
            user_game_session = UserGameSessionModel.objects.filter(game_session_id=session_id)

            # находим у кого максимальное колиечество баллов и не сдался- победитель
            max_score = 0

            for obj in user_game_session:
                if obj.scores > max_score:
                    max_score = obj.scores
                    color_winner = obj.color


            for obj in user_game_session:
                obj.active = False
                obj.status = UserStatus("disconnected")
                # максимальное число баллов и игрок не сдался
                if obj.color == color_winner and obj.color != cur_color:
                    obj.is_winner = True
                else:
                    obj.is_winner = False
                # начисление очков
                scores = int(obj.scores)
                score_table = UserScoresModel.objects.get(user_id=user_id)
                score_table.scores += scores
            # обновление при изменении статуса пользователя
            self.return_user_info_list(content)

    def piece_generation(self, session_id):
        pieces_list=[]
        # белый цвет
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("queen"), color=PieceColor("white"), position='I8'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("king"), color=PieceColor("white"), position='D8'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("rook"), color=PieceColor("white"), position='A8'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("rook"), color=PieceColor("white"), position='L8'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("white"), position='J8'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("white"), position='C8'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("knight"), color=PieceColor("white"), position='B8'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("knight"), color=PieceColor("white"), position='K8'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"), position='A7'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"), position='B7'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"), position='C7'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"), position='D7'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"), position='I7'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"), position='J7'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"), position='K7'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"), position='L7'))

        # черный цвет
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("queen"), color=PieceColor("black"), position='E12'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("king"), color=PieceColor("black"), position='I12'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("rook"), color=PieceColor("black"), position='H12'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("rook"), color=PieceColor("black"), position='L12'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("black"), position='F12'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("black"), position='J12'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("knight"), color=PieceColor("black"), position='G12'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("knight"), color=PieceColor("black"), position='K12'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"), position='L11'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"), position='K11'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"), position='J11'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"), position='I11'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"), position='E11'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"), position='F11'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"), position='G11'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"), position='H11'))

        # красный цвет
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("queen"), color=PieceColor("red"), position='D1'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("king"), color=PieceColor("red"), position='E1'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("rook"), color=PieceColor("red"), position='A1'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("rook"), color=PieceColor("red"), position='H1'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("red"), position='C1'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("red"), position='F1'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("knight"), color=PieceColor("red"), position='B1'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("knight"), color=PieceColor("red"), position='G1'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"), position='A2'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"), position='B2'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"), position='C2'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"), position='D2'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"), position='E2'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"), position='F2'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"), position='G2'))
        pieces_list.append(Piece(game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"), position='H2'))





