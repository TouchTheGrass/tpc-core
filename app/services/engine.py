from typing import List

from app.entities.game_session import GameSessionEntity
from app.entities.piece import PieceEntity
from app.models.enumerations.game_session_status import GameSessionStatus
from app.services.chess_classes.Board import Board
from app.models.piece import PieceModel
from app.models.piece import GameSessionModel

class EngineService:

    def create_game_session(self) -> GameSessionEntity:
        # TODO
        raise NotImplementedError

    def get_game_session_status(self) -> GameSessionStatus:
        # TODO
        raise NotImplementedError

    def get_pieces(self, session_id: int) -> List[PieceEntity]:
        positions = PieceModel.objects.filter(game_session=session_id)
        return positions

    def get_possible_moves(self, piece_id: int) -> List[str]:
        # получим позицию фигуры по id
        piece_position = PieceModel.objects.get(id=piece_id).position
        # получим игровую сессию фигуры по id
        session = PieceModel.objects.get(id=piece_id).game_session
        # получим список положения фигур [[type, colour, position, game_session], ... ] для создания объекта доски
        positions = PieceModel.objects.filter(game_session=session)
        # создаем доску для игры
        self.board = Board(positions)
        possible_moves=self.board.display_legal_moves_for_engine(piece_position)
        return possible_moves


    def move_piece(self, piece_id: int, position: str) -> List[PieceEntity]:
        # получим позицию фигуры по id
        start_position=PieceModel.objects.get(id=piece_id).position
        # получим игровую сессию фигуры по id
        session=PieceModel.objects.get(id=piece_id).game_session
        # получим список положения фигур [[type, colour, position, game_session], ... ] для создания объекта доски
        positions=PieceModel.objects.filter(game_session=session)
        # создаем доску для игры
        board=Board(positions)
        # делаем ход на созданной доске
        res=board.make_move(start_position, position)
        # съеденных фигур нет, если res=0
        if res==0:
            # изменим значение position у фигуры
            PieceModel.objects.get(id=piece_id).position=position
        # res - объект съеденной фигуры
        else:
            # изменим значение position у фигуры
            PieceModel.objects.get(id=piece_id).position = position
            # удалить из бд съеденную фигуру данной сессии, указанного цвета и типа
            PieceModel.objects.filter(game_session=session, type=res.get_type().name, color=res.get_colour().name).delete()
            # добавить возможность поменять статус игрока
            # добавить возможность вносить изменения о положении фигур при рокировке
        # если ход невозможен, вызываем исключение

