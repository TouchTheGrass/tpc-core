from typing import List
from chess_classes.Piece import Piece
from app.entities.game_session import GameSessionEntity
from app.entities.piece import PieceEntity
from app.models.enumerations.game_session_status import GameSessionStatus
from app.services.chess_classes.Board import Board
from app.models.piece import PieceModel
from app.models.piece import GameSessionModel
from app.models.player_game_session import PlayerGameSessionModel
from app.models.enumerations.player_status import PlayerStatus
from app.models.enumerations.piece_type import PieceType


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
        board = Board(positions)
        possible_moves=board.display_legal_moves_for_engine(piece_position)
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
        # съеденных фигур и особых операций в виде повышения пешки и рокировки нет, если len(res)=0
        if len(res)==0:
            # изменим значение position у фигуры
            PieceModel.objects.get(id=piece_id).position=position
        # res - список данных для изменения БД
        # съедание фигуры
        elif len(res)==1:
            # изменим значение position у фигуры
            PieceModel.objects.get(id=piece_id).position = position
            # удалить из бд съеденную фигуру данной сессии, указанного цвета и типа
            PieceModel.objects.filter(game_session=session, type=res[0].get_type().name, color=res[0].get_colour().name).delete()
            # если съеден король, поменять статус игры
            if res[0].get_type()==PieceType.KING:
                GameSessionModel.objects.filter(id=session).status = GameSessionStatus.COMPLETED
        # рокировка
        elif len(res)==2:
            # изменение position для короля
            PieceModel.objects.get(id=piece_id).position = position
            # изменим position для ладьи
            PieceModel.objects.get(game_session=session, type=res[0].get_type().name, color=res[0].get_colour().name)\
                .position=res[1]
        # повышение пешки
        elif len(res)==3:
            # меняем тип фигуры на QUEEN
            PieceModel.objects.get(id=piece_id).type=PieceType.QUEEN
        # поменять статус игрока данной сессии и текущего цвета на ожидание
        PlayerGameSessionModel.objects.get(session_id=session, color=PieceModel.objects.get(id=piece_id).color).status=PlayerStatus.WAIT
        # если ход невозможен, вызываем исключение


