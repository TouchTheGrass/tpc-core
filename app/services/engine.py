from typing import List
from app.services.chess_classes.Board import Board
from app.models.piece import GameSessionModel
from app.models.player_game_session import PlayerGameSessionModel
from app.models.enumerations.player_status import PlayerStatus
from app.models.enumerations.piece_type import PieceType
from app.services.chess_classes.piece_type import PieceTypeEngine
from app.services.chess_classes.color import PieceColorEngine
from app.models.enumerations.piece_color import PieceColor


class EngineService:

    def get_possible_moves(self, session_id: int, piece_id: int) -> List[str]:
        # получим список фигур игровой сессии
        pieces_list = games[session_id].pieces
        for obj in pieces_list:
            if obj.id == piece_id:
                piece_position = obj.position
        # переводим объекты из объектов Piece в формат для работы доски [[piece type, piece colour, position], ... ]
        pieces_list = self.board_list_forming(pieces_list)
        # создаем доску для игры
        board = Board(pieces_list)
        possible_moves = board.display_legal_moves_for_engine(piece_position)
        return possible_moves

    def move_piece(self, session_id: int, piece_id: int, position: str):
        # получим список фигур игровой сессии
        pieces_list = games[session_id].pieces
        for obj in pieces_list:
            if obj.id == piece_id:
                # получаем объект фигуры
                piece_obj = obj
                # получаем позицию фигуры
                piece_position = obj.position
                # получим цвет фигуры в виде "white"
                piece_color = obj.color.value
        # переводим объекты из объектов Piece в формат для работы доски [[piece type, piece colour, position], ... ]
        pieces_list = self.board_list_forming(pieces_list)
        # создаем доску для игры
        board = Board(pieces_list)
        # делаем ход на созданной доске
        res = board.make_move(piece_position, position)
        # съеденных фигур и особых операций в виде повышения пешки и рокировки нет, если len(res)=0
        if len(res) == 0:
            # изменим значение position у фигуры
            piece_obj.position = position
        # res - список данных для изменения БД
        # съедение фигуры
        elif len(res) == 1:
            # изменим значение position у фигуры
            piece_obj.position = position
            # получим съеденную объект съеденной фигуры и удалим его
            for obj in pieces_list:
                if obj.color == PieceColor(res[0].get_colour().value[1]) and obj.type == PieceType(
                        res[0].get_type().value):
                    del obj
            # добавление очков за съеденные фигуры
            self.adding_points(session_id, PieceColor(piece_color), res[0].get_type())
            # если съеден король, поменять статус игры
            if res[0].get_type() == PieceTypeEngine.KING:
                # player_info status становится win и lose
                players_list = games[session_id].players
                for obj in players_list:
                    if obj.status == PlayerStatus("current_turn"):
                        obj.status = PlayerStatus("win")
                    else:
                        obj.status = PlayerStatus("lose")

                # user_game_session active становится False
                user_game_session_list = UserGameSessionModel.objects.filter(game_session_id=session_id, active=True)
                for obj in user_game_session_list:
                    obj.active = False
                    obj.status = UserStatus("disconnected")
                    # если цвет текущего игрока соответствует цвету UserGameSessionModel
                    if obj.color == PieceColor(piece_color):
                        obj.is_winner = True
                        obj.scores += 50
                    else:
                        obj.is_winner = False
                    scores_table = UserScoresModel.objects.get(user_id=obj.user_id)
                    scores_table.scores += obj.scores

                # session status -completed
                game_session_obj = GameSessionModel.objects.filter(id=session_id)
                game_session_obj.status = SessionStatus("completed")

        # рокировка
        elif len(res) == 2:
            pieces_list = games[session_id].pieces
            for obj in pieces_list:
                # изменение position для короля
                if obj.id == piece_id:
                    # obj- объект фигуры короля
                    obj.position = position
                # изменим position для ладьи
                elif obj.type == PieceType(res[0].get_type().value) and obj.color == PieceColor(
                        res[0].get_colour().value):
                    # obj- объект фигуры переставляемой ладьи
                    # res[1] - позиция ладьи
                    obj.position = res[1]

        # повышение пешки
        elif len(res) == 3:
            # меняем тип фигуры на QUEEN
            pieces_list = games[session_id].pieces
            for obj in pieces_list:
                if obj.id == piece_id:
                    # изменение position для пешки
                    obj.position = position
                    # меняем тип фигуры на QUEEN
                    obj.type = PieceType("queen")

    # for_color в формате строки
    def check_and_checkmate(self, session_id: int, for_color):
        # получим список фигур игровой сессии
        pieces_list = games[session_id].pieces
        # переводим объекты из объектов Piece в формат для работы доски [[piece type, piece colour, position], ... ]
        pieces_list = self.board_list_forming(pieces_list)
        # создаем доску для игры
        board = Board(pieces_list)
        colors = ["white", "red", "black"]
        check_and_checkmate_dict = {}
        for obj in colors:
            check_and_checkmate_dict[PieceColor(obj)] = board.is_check_and_checkmate(PieceColorEngine(obj))

        # returns: 1: ни шах, и не мат; 2: шах; 3: мат
        # return: {PieceColor("white"): 1}
        return check_and_checkmate_dict

    def adding_points(self, session_id, cur_color, eaten_piece_type):
        user_game_session_list = UserGameSessionModel.objects.filter(game_session_id=session_id, active=True)
        for obj in user_game_session_list:
            if obj.color == cur_color:
                if eaten_piece_type == PieceTypeEngine.ROOK or eaten_piece_type == PieceTypeEngine.BISHOP or eaten_piece_type == PieceTypeEngine.KNIGHT:
                    obj.scores += 10
                elif eaten_piece_type == PieceTypeEngine.PAWN:
                    obj.scores += 1
                elif eaten_piece_type == PieceTypeEngine.QUEEN:
                    obj.scores += 25

    # метод для формирования из списка, содержащего объекты Piece в формат для движка [[PieceType, PieceColor, position],..]
    def board_list_forming(list):
        board_list = []
        for obj in list:
            board_list.extend([[PieceTypeEngine(obj.type.value), PieceColorEngine(obj.color.value[1]), obj.position]])
        return board_list

