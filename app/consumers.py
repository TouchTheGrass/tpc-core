import datetime
import json
import time
import uuid
from threading import Thread

from channels.exceptions import DenyConnection
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser

from app.enumerations.game_session_status import GameSessionStatus
from app.enumerations.piece_color import PieceColor
from app.enumerations.piece_type import PieceType
from app.enumerations.player_status import PlayerStatus
from app.enumerations.user_status import UserStatus
from app.models import GameSession, UserGameSession, User, UserScores
from app.services.engine import EngineService
from app.services.games import games, GameInfo, PlayerInfo, Piece


class LobbyListWebsocket(WebsocketConsumer):

    def connect(self):
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data):
        command = json.loads(text_data)
        if command.get("type") == 'lobby_list':
            self.lobby_list()

    def lobby_list(self):
        # отправка спичка свободных лобби
        self.send(text_data=json.dumps({
            'LobbyList': self.get_list_of_available_lobbies()
        }))

    def get_list_of_available_lobbies(self):
        # доступны лобби у которых game_session status -wait
        lobby_list = []
        waiting_game_sessions = GameSession.objects.filter(status=GameSessionStatus("wait"))
        for el in waiting_game_sessions:
            # id игровой сессии
            game_session_id = el.id
            # получаем объекты участников конкретной сессии
            users = UserGameSession.objects.filter(game_sessiion_id=el.id)
            # получим id игроков
            players_id = []
            for pl in users:
                players_id.append(pl.user_id)
            lobby_item = {"game_session_id": game_session_id, "players": players_id}
            lobby_list.append(lobby_item)

        return lobby_list


class InteractionWithTheLobby(WebsocketConsumer):
    # соединение хранит id соединенного пользователя и id ранее упомянутой game_session
    # при успешном соединении user_game_session.status = not_ready
    def connect(self):
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection("Такого пользователя не существует")
        self.accept()

    def disconnect(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True)
        session_id = user_game_session[0].game_session_id

        # если пользователь имеет активную user_game_session и game_session.status == wait
        if user_game_session.exists() == True and \
                GameSession.objects.get(id=session_id).status == GameSessionStatus("wait"):
            user_game_session.delete()
        # если пользователь имеет активную user_game_session и game_session.status == game
        if user_game_session.exists() == True and \
                GameSession.objects.get(id=session_id).status == GameSessionStatus("game"):
            user_game_session[0].status = UserStatus("disconnected")
            # если активная user_game_session имеет статус disconnected более 60 секунд
            # таймер запускается в отдельном потоке
            game_end = Thread(target=self.game_end_timer)
            game_end.start()

    def receive(self, text_data):
        comand = json.loads(text_data)
        user_id = self.scope["user"]
        contant = {"user-id": user_id}
        if comand.get("type") == 'request':
            if comand.get("value") == "create_lobby":
                self.create_lobby(contant)
            elif comand.get("value") == "consider":
                self.consider(contant)
            elif comand.get("value") == "disconnect":
                self.disconnect(contant)

        elif comand.get("type") == "connect_lobby":
            session_id = comand.get("game_session_id")
            content = {"user_id": user_id, "session_id": session_id}
            self.connect_lobby(content)

        elif comand.get("type") == "change_color":
            color = comand.get("value")
            content = {"user_id": user_id, "color": color}
            self.change_color(content)

        elif comand.get("type") == "change_readiness":
            user_status = comand.get("value")
            contant = {"user_id": user_id, "status": user_status}
            self.change_readiness(contant)

        elif comand.get("type") == "move_piece":
            position = comand.get("position")
            piece_id = comand.get("id")
            contant = {"user_id": user_id, "piece_id": piece_id, "position": position}
            self.move_piece(contant)

        elif comand.get("type") == "game_session":
            contant = {"user_id": user_id}
            self.return_game_session_info(contant)

        elif comand.get("type") == "user_info_list":
            contant = {"user_id": user_id}
            self.return_user_info_list(contant)

        elif comand.get("type") == "player_info_list":
            contant = {"user_id": user_id}
            self.return_player_info_list(contant)

        elif comand.get("type") == "piece_list":
            contant = {"user_id": user_id}
            self.retur_piece_list(contant)

        elif comand.get("type") == "possible_moves_list":
            contant = {"user_id": user_id}
            self.possible_moves_list(contant)

    # ________________________________________________________________________________
    # Подключенным пользователям требуется предоставлять следующие данные
    # ________________________________________________________________________________
    # Предоставление информации об активной game_session
    def return_game_session_info(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'GameSession': None
            }))
        # у пользователя есть уникальная запись user_game_session -> отправляется информация об активной game_session
        # обновление должно происходить при изменении статуса игровой сессии
        else:
            game_id = user_game_session[0].game_session_id
            game_session_obj = GameSession.objects.get(id=game_id)
            self.send(text_data=json.dumps({
                'GameSession': {"id": game_session_obj.id, "status": game_session_obj.status.value}
            }))

    # Предоставление списка user_gamer_session, ссылающихся на активную game_session
    # обновление должно происходить при изменении информации о пользователей текущей сессии:
    # при добавлении/удалении пользователя
    # при изменении статуса пользователя
    # при изменении цвета пользователем
    def return_user_info_list(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True)
        # у пользователя нет активной записи user_game_session
        if not user_game_session.exists():
            self.send(text_data=json.dumps({
                'UserInfoList': None
            }))
        else:
            game_id = user_game_session[0].game_session_id
            user_list = UserGameSession.objects.filter(game_session_id=game_id)
            user_info_list = []
            for obj in user_list:
                user_name = User.objects.get(id=obj.user_id).name
                user_info_list.append(
                    {"id": obj.id, "name": user_name, "rating": obj.scores, "status": obj.status.value,
                     "color": obj.color.value})

            self.send(text_data=json.dumps({
                'UserInfoList': user_info_list
            }))

    # Предоставление списка player_info
    # обновляется в случае изменения внутриигрового статуса
    def return_player_info_list(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'PlayerInfoList': None
            }))
        else:
            game_id = user_game_session[0].game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSession.objects.filter(id=game_id, status=GameSessionStatus("game")).exists() == False:
                self.send(text_data=json.dumps({
                    'PlayerInfoList': None
                }))
            else:
                # у пользователя есть активная user_game_session, у которой status == game
                player_info_list = []

                player_list = games[game_id].players

                for obj in player_list:
                    player_info_list.append({"id": obj.user_id, "status": obj.status.value})

                self.send(text_data=json.dumps({
                    'PlayerInfoList': player_info_list
                }))

    # Предоставление списка piece
    # обновляется при изменении данных фигуры:
    # тип
    # позиция
    # цвет
    def retur_piece_list(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'PieceList': None
            }))
        else:
            game_id = user_game_session[0].game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSession.objects.filter(id=game_id, status=GameSessionStatus("game")).exists() == False:
                self.send(text_data=json.dumps({
                    'PieceList': None
                }))
            else:
                # у пользователя есть активная user_game_session, у которой status == game
                obj_piece_list = []

                piece_list = games[game_id].pieces

                for obj in piece_list:
                    obj_piece_list.append({"id": obj.id, "type": obj.type.value, "color": obj.color.value,
                                           "position": obj.position.value})

                self.send(text_data=json.dumps({
                    'PieceList': obj_piece_list
                }))

    # Предоставление списка доступных ходов
    # обновляется после каждого хода
    def possible_moves_list(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True)
        # цвет за который играет пользователь
        color_value = user_game_session[0].color.value
        session_id = user_game_session[0].game_session_id

        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'PossibleMovesList': None
            }))
        else:
            game_id = user_game_session[0].game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSession.objects.filter(id=game_id, status=GameSessionStatus("game")).exists() == False:
                self.send(text_data=json.dumps({
                    'PossibleMovesList': None
                }))
            else:
                # у пользователя есть активная user_game_session, у которой status == game
                possible_moves_list = []
                our_pieces_id = []
                # получаем все фигуры пользователя
                # получаем список ВСЕХ фигур данной игровой сессии
                all_pieces = games[session_id].pieces
                # obj - объект Piece
                for obj in all_pieces:
                    # добавляем id фигур нашего цвета в список
                    if obj.color.value == color_value:
                        our_pieces_id.append(id(obj))

                for piece_id in our_pieces_id:
                    available_move_list = EngineService.get_possible_moves(session_id, piece_id)
                    possible_moves_item = {"piece_id": piece_id, "possible_moves": available_move_list}
                    possible_moves_list.append(possible_moves_item)

                self.send(text_data=json.dumps({
                    'PossibleMovesList': possible_moves_list
                }))

    # ________________________________________________________________________________
    # от подключенных требуется обрабатывать следующие запросы:
    # ________________________________________________________________________________

    # запрос на присоединение к лобби
    def connect_lobby(self, content):
        user_id = content["user_id"]
        session_id = content["session_id"]
        if GameSession.objects.get(id=session_id).status == GameSessionStatus("wait"):
            # если нет активных game_session у инициализатора и
            # связанных с game_session user_game_session менее 3
            if UserGameSession.objects.filter(user_id=user_id, active=True).exists() == False and \
                    len(UserGameSession.objects.filter(game_session_id=session_id)) < 3:
                user_game_session = UserGameSession(
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
                'Connection': {"game_session_id": session_id}
            }))
        # если у подключаемой game_session status == game
        if GameSession.objects.get(id=session_id).status == GameSessionStatus("game"):
            # требуется наличие активной game_session у инициализатора
            if UserGameSession.objects.filter(user_id=user_id, game_session_id=session_id, active=True).exists():
                user_game_session = UserGameSession.objects.filter(
                    user_id=user_id,
                    game_session_id=session_id,
                    active=True)
                user_game_session[0].status = UserStatus("playing")

                self.send(text_data=json.dumps({
                    'Connection': {"game_session_id": session_id}
                }))
        # обновление при изменении статуса игровой сессии
        self.return_game_session_info(user_id)
        # обновление при добавлении/удалении пользователя
        self.return_user_info_list(user_id)

    # запрос на создание лобби
    def create_lobby(self, content):
        user_id = content["user_id"]
        # отсутствие активной game_session у инициализатора
        if not UserGameSession.objects.filter(user_id=user_id, active=True).exists():
            game_session = GameSession(
                status=GameSessionStatus("wait")
            )
            game_session.save()
            session_id = game_session.id
            # создание объектов фигур и их расстановка
            pieces_list = self.piece_generation(session_id)

            games[session_id] = GameInfo(
                players=[
                    PlayerInfo(
                        user_id=user_id,
                        game_session_id=session_id,
                        player_status=PlayerStatus("wait_turn"))],
                pieces=[pieces_list])

            user_game_session = UserGameSession(
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
        color = PieceColor(content["color"])
        # требуется активная user_gamer_session у пользователя
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True)
        session_id = user_game_session[0].game_session_id
        if user_game_session.exists():
            # получаем доступные цвета
            user_gamer_session = UserGameSession.objects.filter(game_session_id=session_id)
            for obj in user_gamer_session:
                if obj.color.value == color:
                    # Такой цвет нельзя выбрать
                    self.send(text_data=json.dumps({
                        'Color': None
                    }))
            user_game_session[0].color = PieceColor(color)
            self.send(text_data=json.dumps({
                'Color': {"value": color}
            }))
        # обновление при изменении цвета пользователем
        self.return_user_info_list(content)

    # смена статуса о готовности для текущего пользователя
    def change_readiness(self, content):
        user_id = content["user_id"]
        # user_status - строка
        user_status = content["status"]
        # требуется активная user_gamer_session у пользователя
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True)
        session_id = user_game_session[0].game_session_id
        if user_game_session.exists():
            user_game_session[0].status = UserStatus(user_status)
        self.send(text_data=json.dumps({
            'ReadyStatus': {"value": user_status}
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
        position = content["position"]
        piece_id = content["piece_id"]
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True)
        session_id = user_game_session[0].game_session_id
        # если есть активная user_game_session у пользователя и game_session.status == game
        if user_game_session.exists() == True and GameSession.objects.filter(id=session_id, status=GameSessionStatus(
                "game")).exists() == True:
            # требуется player_info.status == current_turn
            list_player_info = games[session_id].players
            pieces = games[session_id].pieces

            # obj- объект PlayerInfo
            for obj in list_player_info:
                # находим текущего пользователя
                if obj.user_id == user_id:
                    if obj.player_status == PlayerStatus("current_turn"):
                        # параметры связанных piece меняются в соответствии с правилами
                        EngineService.move_piece(session_id, piece_id, position)
                        # параметры player_info меняются в соответствии с правилами

            self.send(text_data=json.dumps({
                'PieceMove': {"id": piece_id, "position": position}
            }))

            # обновляется в случае изменения внутриигрового статуса
            self.return_player_info_list(content)
            # обновляется при изменении данных фигуры
            self.retur_piece_list(content)
            # обновляется после каждого хода
            self.possible_moves_list(content)

    # запрос сдаться
    def consider(self, content):
        user_id = content["user_id"]
        # требуется активная user_game_session у пользователя и
        # требуется user_game_session.status == game
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True, status=UserStatus("playing"))
        session_id = user_game_session[0].game_session_id
        cur_color = user_game_session[0].color
        if user_game_session.exists():
            # игра заканчивается
            game_session = GameSession.objects.get(id=session_id)
            game_session.status = GameSessionStatus("completed")
            # обновление при изменении статуса игровой сессии
            self.return_game_session_info(user_id)
            # user_game_session у игроков данной сессии становятся неактивными
            user_game_session = UserGameSession.objects.filter(game_session_id=session_id)
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
                score_table = UserScores.objects.get(user_id=user_id)
                score_table.scores += scores
        # обновление при изменении статуса пользователя
        self.return_user_info_list(user_id)

    # вспомогательный метод на изменение статуса игры на game с контролем условий:
    # существует 3 user_game_session связанных с game_session
    # все user_game_session связанные с game_session имеют статус ready
    # game_session.status == wait
    def changing_game_status_to_game(self, game_session_id):
        game_session_obj = GameSession.objects.get(id=game_session_id)
        user_game_session_list = UserGameSession.objects.filter(game_session_id=game_session_id)
        if game_session_obj.status == GameSessionStatus("wait") and \
                len(user_game_session_list) == 3:
            for obj in user_game_session_list:
                if obj.status != UserStatus("ready"):
                    return 0
            game_session_obj.status = GameSessionStatus("game")

    def game_end_timer(self, content):
        user_id = content["user_id"]
        time.sleep(60)
        # если активная user_game_session имеет статус disconnected, игра заканчивается
        user_game_session = UserGameSession.objects.filter(user_id=user_id, active=True)
        session_id = user_game_session[0].game_session_id
        cur_color = user_game_session[0].color
        if user_game_session[0].status == UserStatus("disconnected"):
            # игра заканчивается
            game_session = GameSession.objects.get(id=session_id)
            game_session.status = GameSessionStatus("completed")
            # обновление при изменении статуса игровой сессии
            self.return_game_session_info(content)
            # user_game_session у игроков данной сессии становятся неактивными
            user_game_session = UserGameSession.objects.filter(game_session_id=session_id)

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
                score_table = UserScores.objects.get(user_id=user_id)
                score_table.scores += scores
            # обновление при изменении статуса пользователя
            self.return_user_info_list(content)

    def piece_generation(self, session_id):
        return [
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("queen"), color=PieceColor("white"),
                  position='I8'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("king"), color=PieceColor("white"),
                  position='D8'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("rook"), color=PieceColor("white"),
                  position='A8'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("rook"), color=PieceColor("white"),
                  position='L8'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("white"),
                  position='J8'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("white"),
                  position='C8'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("knight"), color=PieceColor("white"),
                  position='B8'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("knight"), color=PieceColor("white"),
                  position='K8'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"),
                  position='A7'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"),
                  position='B7'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"),
                  position='C7'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"),
                  position='D7'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"),
                  position='I7'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"),
                  position='J7'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"),
                  position='K7'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("white"),
                  position='L7'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("queen"), color=PieceColor("black"),
                  position='E12'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("king"), color=PieceColor("black"),
                  position='I12'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("rook"), color=PieceColor("black"),
                  position='H12'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("rook"), color=PieceColor("black"),
                  position='L12'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("black"),
                  position='F12'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("black"),
                  position='J12'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("knight"), color=PieceColor("black"),
                  position='G12'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("knight"), color=PieceColor("black"),
                  position='K12'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"),
                  position='L11'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"),
                  position='K11'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"),
                  position='J11'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"),
                  position='I11'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"),
                  position='E11'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"),
                  position='F11'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"),
                  position='G11'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("black"),
                  position='H11'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("queen"), color=PieceColor("red"),
                  position='D1'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("king"), color=PieceColor("red"),
                  position='E1'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("rook"), color=PieceColor("red"),
                  position='A1'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("rook"), color=PieceColor("red"),
                  position='H1'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("red"),
                  position='C1'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("bishop"), color=PieceColor("red"),
                  position='F1'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("knight"), color=PieceColor("red"),
                  position='B1'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("knight"), color=PieceColor("red"),
                  position='G1'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"),
                  position='A2'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"),
                  position='B2'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"),
                  position='C2'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"),
                  position='D2'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"),
                  position='E2'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"),
                  position='F2'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"),
                  position='G2'),
            Piece(id=int(uuid.uuid4()), game_session_id=session_id, type=PieceType("pawn"), color=PieceColor("red"),
                  position='H2')]
        # белый цвет

        # черный цвет

        # красный цвет
