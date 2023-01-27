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
from ..app.models.enumerations.position import Position
from ..app.models.enumerations.game_session_status import GameSessionStatus
from ..app.dto.piece_movement import PieceMovement
from ..app.dto.game_session import GameSession
from ..app.dto.ready_status import ReadyStatus
from ..app.dto.game_info import GameInfo
from ..app.dto.сolor import Color
from ..app.dto.connection import Connection
from ..app.dto.lobby_item import LobbyItem
from ..app.dto.piece_item import PieceItem
from ..app.dto.player_info_item import PlayerInfoItem
from ..app.dto.possible_move_item import PossibleMoveItem
from ..app.dto.user_info_item import UserInfoItem




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
        session_id = user_game_session.game_session_id

        # если пользователь имеет активную user_game_session и game_session.status == wait
        if user_game_session==True and\
            GameSessionModel.objects.get(id=session_id).status == GameSessionStatus("wait"):
                user_game_session.delete()
        # если пользователь имеет активную user_game_session и game_session.status == game
        if user_game_session == True and \
                GameSessionModel.objects.get(id=session_id).status == GameSessionStatus("game"):
                    user_game_session.status=UserStatus("disconnected")
                    # если активная user_game_session имеет статус disconnected более 60 секунд
                    # таймер запускается в отдельном потоке
                    game_end = Thread(target=self.game_end_timer)
                    game_end.start()

    # ________________________________________________________________________________
    # Подключенным пользователям требуется предоставлять следующие данные
    #________________________________________________________________________________
    # Предоставление информации об активной game_session
    def GameSession(self, content):
        user_id=content["user_id"]
        user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists()==False:
            self.send(text_data=json.dumps({
                'user_game_session': None
            }))
        # у пользователя есть уникальная запись user_game_session -> отправляется информация об активной game_session
        # обновление должно происходить при изменении статуса игровой сессии
        else:
            game_id=user_game_session.game_session_id
            game_session_obj=GameSessionModel.objects.get(id=game_id)
            self.send(text_data=json.dumps({
                'GameSession':GameSession(id=game_session_obj.id, status=game_session_obj.status)
            }))

    # Предоставление списка user_gamer_session, ссылающихся на активную game_session
    # обновление должно происходить при изменении информации о пользователей текущей сессии:
    # при добавлении/удалении пользователя
    # при изменении статуса пользователя
    # при изменении цвета пользователем
    def  UserInfoList(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'UserInfoList': None
            }))
        else:
            game_id = user_game_session.game_session_id
            user_list=UserGameSessionModel.objects.filter(game_session_id=game_id)
            UserInfoList=[]
            for obj in user_list:
                user_name=UserModel.objects.get(id=obj.user_id).name
                UserInfoList.append(UserInfoItem(id=obj.id, name=user_name, status=obj.status, color=obj.color))

            self.send(text_data=json.dumps({
                'UserInfoList':UserInfoList
            }))

    # Предоставление списка player_info
    # обновляется в случае изменения внутриигрового статуса
    def PlayerInfoList(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'PlayerInfoList': None
            }))
        else:
            game_id=user_game_session.game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSessionModel.objects.filter(id=game_id, status=GameSessionStatus("game")).exists()==False:
                self.send(text_data=json.dumps({
                    'PlayerInfoList': None
                }))
            else:
                # у пользователя есть активная user_game_session, у которой status == game
                PlayerInfoList=[]
                player_list=games[game_id].players
                for obj in player_list:
                    PlayerInfoList.append(PlayerInfoItem(id=obj.user_id,status=obj.status))
                self.send(text_data=json.dumps({
                    'PlayerInfoList': PlayerInfoList
                }))

    # Предоставление списка piece
    # обновляется при изменении данных фигуры:
    # тип
    # позиция
    # цвет
    def PieceList(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'PieceList': None
            }))
        else:
            game_id = user_game_session.game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSessionModel.objects.filter(id=game_id, status=GameSessionStatus("game")).exists() == False:
                self.send(text_data=json.dumps({
                    'PieceList': None
                }))
            else:
                # у пользователя есть активная user_game_session, у которой status == game
                PieceList=[]
                piece_list=games[game_id].pieces
                for obj in piece_list:
                    PieceList.append(PieceItem(id=obj.id,type=obj.type,color=obj.color,position=obj.position))
                self.send(text_data=json.dumps({
                    'PieceList': PieceList
                }))

    # Предоставление списка доступных ходов
    # обновляется после каждого хода
    def PossibleMoveList(self, content):
        user_id = content["user_id"]
        piece_id=content["piece_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id)
        session_id=user_game_session.game_session_id
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'PossibleMoveList': None
            }))
        else:
            game_id = user_game_session.game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSessionModel.objects.filter(id=game_id, status=GameSessionStatus("game")).exists() == False:
                self.send(text_data=json.dumps({
                    'PossibleMoveList': None
                }))
            else:
                PossibleMoveList=[]
                # у пользователя есть активная user_game_session, у которой status == game
                available_move_list=EngineService.get_possible_moves(session_id, piece_id)
                for obj in available_move_list:
                    PossibleMoveList.append(PossibleMoveItem(value=Position(obj)))
                self.send(text_data=json.dumps({
                    'PossibleMoveList': PossibleMoveList
                }))

    # ________________________________________________________________________________
    # от подключенных требуется обрабатывать следующие запросы:
    # ________________________________________________________________________________

    # запрос на присоединение к лобби
    def ConnectLobby(self, content):
        user_id = content["user_id"]
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

        if GameSessionModel.objects.get(id=session_id).status==GameSessionStatus("game"):
            if UserGameSessionModel.objects.filter(user_id=user_id, game_session_id=session_id,active=True).exists() == True:
                user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, game_session_id=session_id,active=True)
                user_game_session.status=UserStatus("playing")

                self.send(text_data=json.dumps({
                    'Connection': Connection(game_session_id=session_id)
                }))
        # обновление при изменении статуса игровой сессии
        self.return_game_session_info(content)
        # обновление при добавлении/удалении пользователя
        self.return_user_gamer_session_list(content)


    # запрос на создание лобби
    def CreateLobby(self, content):
        user_id = content["user_id"]
        # отсутствие активной game_session у инициализатора
        if UserGameSessionModel.objects.filter(user_id=user_id, active=True).exists() == False:
            game_session=GameSessionModel(
                status=GameSessionStatus("wait")
            )
            game_session.save()
            session_id=game_session.id
            # создание объектов фигур и их расстановка
            pieces_list=self.piece_generation(session_id)

            GameInfo([PlayerInfo(user_id=user_id, game_session_id=session_id, status=PlayerStatus("wait_turn"))],\
                     [pieces_list])
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
        self.return_user_gamer_session_list(content)


    # смена цвета фигур для текущего пользователя
    def ChangeColor(self, content):
        user_id = content["user_id"]
        # color - объект типа PieceColor
        color=content["color"]
        # требуется активная user_gamer_session у пользователя
        user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id=user_game_session.game_session_id
        if user_game_session.exists() == True:
            # получаем доступные цвета
            user_gamer_session = UserGameSessionModel.objects.filter(game_session_id=session_id)
            for obj in user_gamer_session:
                if obj.color == color:
                    # Такой цвет нельзя выбрать
                    self.send(text_data=json.dumps({
                        'Color': None
                    }))
            user_game_session.color=color
            self.send(text_data=json.dumps({
                'Color': Color(value=color)
            }))
        # обновление при изменении цвета пользователем
        self.return_user_gamer_session_list(content)

    # смена статуса о готовности для текущего пользователя
    def ChangeReadiness(self, content):
        user_id = content["user_id"]
        # user_status - объект типа ReadyStatus
        user_status=content["status"]
        # требуется активная user_gamer_session у пользователя
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id=user_game_session.game_session_id
        if user_game_session.exists() == True:
            user_game_session.status=UserStatus(user_status)
        self.send(text_data=json.dumps({
            'ReadyStatus': ReadyStatus(value=user_status)
        }))

        # проверка и изменение статуса game_session на game
        self.changing_game_status_to_game(session_id)
        # обновление при изменении статуса игровой сессии
        self.return_game_session_info(content)
        # обновление при изменении статуса пользователя
        self.return_user_gamer_session_list(content)

    # запрос на передвижение фигуры
    def MovePiece(self, content):
        user_id = content["user_id"]
        piece_id=content["piece_id"]
        position=content["position"]
        user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id = user_game_session.game_session_id
        # если есть активная user_game_session у пользователя и game_session.status == game
        if user_game_session.exists() == True and GameSessionModel.objects.filter(id=session_id, status=GameSessionStatus("game")):
            # требуется player_info.status == current_turn
            list_player_info=games[session_id].players
            for obj in list_player_info:
                if obj.player_status==PlayerStatus("current_turn"):
                    # параметры связанных piece меняются в соответствии с правилами
                    EngineService.move_piece(session_id,piece_id,position)
                    #параметры player_info меняются в соответствии с правилами
            list_piece_info=games[session_id].pieces
            for obj in list_piece_info:
                if obj.id==piece_id:
                    piece_type=obj.type

            self.send(text_data=json.dumps({
                'PieceMovement': PieceMovement(id=piece_id, position=position,promotion= piece_type)
            }))

            # обновляется в случае изменения внутриигрового статуса
            self.return_player_info_list(content)
            # обновляется при изменении данных фигуры
            self.retur_piece_list(content)
            # обновляется после каждого хода
            self.available_moves_list(content)

    # запрос на проверку шаха и мата
    def CheckAndCheckmate(self, content):
        user_id = content["user_id"]
        # требуется активная user_game_session у пользователя и
        # требуется user_game_session.status == game
        user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, active=True, status=UserStatus("playing"))
        if user_game_session.exists() == True:
            # получить id сессии
            session_id=user_game_session.game_session_id
            # получить цвет игрока
            color=user_game_session.color.value
            # check_and_checkmate_dict - {PieceColor("white"): 1}
            # 1: ни шах, и не мат; 2: шах; 3: мат
            check_and_checkmate_dict=EngineService.check_and_checkmate(session_id=session_id, for_color=color)
            self.send(text_data=json.dumps({
                'CheckAndCheckmate': check_and_checkmate_dict
            }))

    # запрос сдаться
    def Consider(self, content):
        user_id = content["user_id"]
        session_id = content["session_id"]
        # требуется активная user_game_session у пользователя и
        # требуется user_game_session.status == game
        if UserGameSessionModel.objects.filter(user_id=user_id, active=True, status=UserStatus("playing")).exists() == True:
            # игра заканчивается
            game_session=GameSessionModel.objects.get(id=session_id)
            game_session.status=GameSessionStatus("completed")
            # обновление при изменении статуса игровой сессии
            self.return_game_session_info(content)
            # user_game_session у игроков данной сессии становятся неактивными
            user_game_session=UserGameSessionModel.objects.filter(game_session_id=session_id)
            for obj in user_game_session:
                obj.active=False
                obj.status=UserStatus("disconnected")
                #is_winner = player_info.status ???
                # начисление очков
                scores=int(obj.scores)
                score_table=UserScoresModel.objects.get(user_id=user_id)
                score_table.scores+=scores
        # обновление при изменении статуса пользователя
        self.return_user_gamer_session_list(content)

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
        session_id=user_game_session.game_session_id
        if user_game_session.status==UserStatus("disconnected"):
            # игра заканчивается
            game_session = GameSessionModel.objects.get(id=session_id)
            game_session.status = GameSessionStatus("completed")
            # обновление при изменении статуса игровой сессии
            self.return_game_session_info(content)
            # user_game_session у игроков данной сессии становятся неактивными
            user_game_session = UserGameSessionModel.objects.filter(game_session_id=session_id)
            for obj in user_game_session:
                obj.active = False
                obj.status = UserStatus("disconnected")
                # is_winner = player_info.status ???
                # начисление очков
                scores = int(obj.scores)
                score_table = UserScoresModel.objects.get(user_id=user_id)
                score_table.scores += scores
            # обновление при изменении статуса пользователя
            self.return_user_gamer_session_list(content)

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





