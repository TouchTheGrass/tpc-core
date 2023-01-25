from channels.generic.websocket import WebsocketConsumer
import json
from channels.exceptions import DenyConnection
from django.contrib.auth.models import AnonymousUser
import datetime
from ..app.services.engine import EngineService
import time
from threading import Thread

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
            GameSessionModel.objects.get(id=session_id).status == SessionStatus("wait"):
                user_game_session.delete()
        # если пользователь имеет активную user_game_session и game_session.status == game
        if user_game_session == True and \
                GameSessionModel.objects.get(id=session_id).status == SessionStatus("game"):
                    user_game_session.status=UserStatus("disconnected")
                    # если активная user_game_session имеет статус disconnected более 60 секунд
                    # таймер запускается в отдельном потоке
                    game_end = Thread(target=self.game_end_timer)
                    game_end.start()

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
    def return_user_gamer_session_list(self, content):
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
    def return_player_info_list(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'user_game_session': None
            }))
        else:
            game_id=user_game_session.game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSessionModel.objects.filter(id=game_id, status=SessionStatus("game")).exists()==False:
                self.send(text_data=json.dumps({
                    'user_game_session': None
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
    def retur_piece_list(self, content):
        user_id = content["user_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id)
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'user_game_session': None
            }))
        else:
            game_id = user_game_session.game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSessionModel.objects.filter(id=game_id, status=SessionStatus("game")).exists() == False:
                self.send(text_data=json.dumps({
                    'user_game_session': None
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
    def available_moves_list(self, content):
        user_id = content["user_id"]
        piece_id=content["piece_id"]
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id)
        session_id=user_game_session.game_session_id
        # у пользователя нет активной записи user_game_session
        if user_game_session.exists() == False:
            self.send(text_data=json.dumps({
                'available_move_list': None
            }))
        else:
            game_id = user_game_session.game_session_id
            # у пользователя нет активной user_game_session, у которой status == game
            if GameSessionModel.objects.filter(id=game_id, status=SessionStatus("game")).exists() == False:
                self.send(text_data=json.dumps({
                    'available_move_list': None
                }))
            else:
                # у пользователя есть активная user_game_session, у которой status == game
                available_move_list=EngineService.get_possible_moves(session_id, piece_id)
                self.send(text_data=json.dumps({
                    'available_move_list': available_move_list
                }))

    # ________________________________________________________________________________
    # от подключенных требуется обрабатывать следующие запросы:
    # ________________________________________________________________________________

    # запрос на присоединение к лобби
    def request_to_join_the_lobby(self, content):
        user_id = content["user_id"]
        session_id=content["session_id"]
        if GameSessionModel.objects.get(id=session_id).status==SessionStatus("wait"):
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

        if GameSessionModel.objects.get(id=session_id).status==SessionStatus("game"):
            if UserGameSessionModel.objects.filter(user_id=user_id, game_session_id=session_id,active=True).exists() == True:
                user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, game_session_id=session_id,active=True)
                user_game_session.status=UserStatus("playing")
        # обновление при изменении статуса игровой сессии
        self.return_game_session_info(content)
        # обновление при добавлении/удалении пользователя
        self.return_user_gamer_session_list(content)


    # запрос на создание лобби
    def request_to_create_the_lobby(self, content):
        user_id = content["user_id"]
        # отсутствие активной game_session у инициализатора
        if UserGameSessionModel.objects.filter(user_id=user_id, active=True).exists() == False:
            game_session=GameSessionModel(
                status=SessionStatus("wait")
            )
            game_session.save()
            session_id=game_session.id

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
    def changing_the_piece_color(self, content):
        user_id = content["user_id"]
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
                        'COLOR': None
                    }))
            user_game_session.color=color
        # обновление при изменении цвета пользователем
        self.return_user_gamer_session_list(content)

    # смена статуса о готовности для текущего пользователя
    def changing_the_status_of_readiness(self, content):
        user_id = content["user_id"]
        user_status=content["status"]
        # требуется активная user_gamer_session у пользователя
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id=user_game_session.game_session_id
        if user_game_session.exists() == True:
            user_game_session.status=UserStatus(user_status)
        # проверка и изменение статуса game_session на game
        self.changing_game_status_to_game(session_id)
        # обновление при изменении статуса игровой сессии
        self.return_game_session_info(content)
        # обновление при изменении статуса пользователя
        self.return_user_gamer_session_list(content)

    # запрос на передвижение фигуры
    def request_to_move_the_piece(self, content):
        user_id = content["user_id"]
        piece_id=content["piece_id"]
        position=content["position"]
        user_game_session=UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id = user_game_session.game_session_id
        # если есть активная user_game_session у пользователя и game_session.status == game
        if user_game_session.exists() == True and GameSessionModel.objects.filter(id=session_id, status=SessionStatus("game")):
            # требуется player_info.status == current_turn
            list_player_info=games[session_id].players
            for obj in list_player_info:
                if obj.player_status==PlayerStatus("current_turn"):
                    # параметры связанных piece меняются в соответствии с правилами
                    EngineService.move_piece(session_id,piece_id,position)
                    #параметры player_info меняются в соответствии с правилами
        # обновляется в случае изменения внутриигрового статуса
        self.return_player_info_list(content)
        # обновляется при изменении данных фигуры
        self.retur_piece_list(content)
        # обновляется после каждого хода
        self.available_moves_list(content)


    # запрос сдаться
    def request_to_surrender(self, content):
        user_id = content["user_id"]
        session_id = content["session_id"]
        # требуется активная user_game_session у пользователя и
        # требуется user_game_session.status == game
        if UserGameSessionModel.objects.filter(user_id=user_id, active=True, status=UserStatus("playing")).exists() == True:
            # игра заканчивается
            game_session=GameSessionModel.objects.get(id=session_id)
            game_session.status=SessionStatus("completed")
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
        if game_session_obj.status==SessionStatus("wait") and\
            len(user_game_session_list)==3:
                for obj in user_game_session_list:
                    if obj.status!=UserStatus("ready"):
                        return 0
                game_session_obj.status=SessionStatus("game")

    def game_end_timer(self, content):
        user_id = content["user_id"]
        time.sleep(60)
        # если активная user_game_session имеет статус disconnected, игра заканчивается
        user_game_session = UserGameSessionModel.objects.filter(user_id=user_id, active=True)
        session_id=user_game_session.game_session_id
        if user_game_session.status==UserStatus("disconnected"):
            # игра заканчивается
            game_session = GameSessionModel.objects.get(id=session_id)
            game_session.status = SessionStatus("completed")
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
