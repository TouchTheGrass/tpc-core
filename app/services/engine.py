from typing import List
from app.entities.piece import PieceEntity
from app.models.enumerations.game_session_status import GameSessionStatus
from app.models.game_session import GameSessionModel
from app.models.piece import PieceModel
from app.models.player_game_session import PlayerGameSessionModel
from app.models.enumerations.player_status import PlayerStatus
from app.models.enumerations.piece_type import PieceType
from app.models.enumerations.piece_color import PieceColor
from app.services.chess_classes.board import Board


class EngineService:

    def get_game_session_status(self, session_id: int) -> GameSessionStatus:
        status = GameSessionModel.objects.get(id=session_id).status
        return status

    def get_pieces(self, session_id: int) -> List[PieceEntity]:
        positions = []
        # достаем элементы фигур
        pieces_of_session = PieceModel.objects.filter(game_session=session_id)
        for el in pieces_of_session:
            positions.append(el.position)
        return positions

    def get_possible_moves(self, piece_id: int) -> List[str]:
        # получим позицию фигуры по id
        piece_position = PieceModel.objects.get(id=piece_id).position
        # получим игровую сессию фигуры по id
        session = PieceModel.objects.get(id=piece_id).game_session
        # получим список положения фигур [[type, color, position, game_session], ... ] для создания объекта доски
        positions = PieceModel.objects.filter(game_session=session)
        # создаем доску для игры
        board = Board(positions)
        possible_moves = board.display_legal_moves_for_engine(piece_position)
        return possible_moves

    def move_piece(self, piece_id: int, position: str):
        # получим позицию фигуры по id
        start_position = PieceModel.objects.get(id=piece_id).position
        # получим цвет фигуры
        piece_colour = PieceModel.objects.get(id=piece_id).color
        # получим игровую сессию фигуры по id
        session = PieceModel.objects.get(id=piece_id).game_session
        # получим id игрока
        player = PlayerGameSessionModel.objects.get(session_id=session, color=piece_colour).player_id
        # получим список положения фигур [[type, colour, position, game_session], ... ] для создания объекта доски
        positions = PieceModel.objects.filter(game_session=session)
        # создаем доску для игры
        board = Board(positions)
        # делаем ход на созданной доске
        res = board.make_move(start_position, position)
        # съеденных фигур и особых операций в виде повышения пешки и рокировки нет, если len(res)=0
        if len(res) == 0:
            # изменим значение position у фигуры
            piece = PieceModel.objects.get(id=piece_id)
            piece.position = position
        # res - список данных для изменения БД
        # съедение фигуры
        elif len(res) == 1:
            # добавим очки игроку
            # self.adding_points(session, player, res[0])
            # изменим значение position у фигуры
            piece = PieceModel.objects.get(id=piece_id)
            piece.position = position
            # удалить из бд съеденную фигуру данной сессии, указанного цвета и типа
            PieceModel.objects.filter(game_session=session, type=res[0].get_type().name,
                                      color=res[0].get_color().name).delete()
            # если съеден король, поменять статус игры
            if res[0].get_type() == PieceType.KING:
                game_status = GameSessionModel.objects.filter(id=session)
                game_status.status = GameSessionStatus.COMPLETED
                # у остальных игроков (проигравших) снять 50 очков
                # self.subtraction_points(session, piece_colour)

        # рокировка
        elif len(res) == 2:
            # изменение position для короля
            king_piece = PieceModel.objects.get(id=piece_id)
            king_piece.position = position
            # изменим position для ладьи
            rook_piece = PieceModel.objects.get(game_session=session, type=res[0].get_type().name,
                                                color=res[0].get_colour().name)
            start_rook_pos = rook_piece.position
            rook_piece.position = res[1]
            # записать ход ладьи в историю
            # self.write_session_motion(rook_piece.id, start_rook_pos, rook_piece.position)
        # повышение пешки
        elif len(res) == 3:
            # меняем тип фигуры на QUEEN
            pawn_piece = PieceModel.objects.get(id=piece_id)
            pawn_piece.type = PieceType.QUEEN
        # Записать ход в историю
        # self.write_session_motion(piece_id,start_position, position)
        # поменять статус игрока данной сессии из текущего цвета на ожидание
        cur_player = PlayerGameSessionModel.objects.get(session_id=session,
                                                        color=PieceModel.objects.get(id=piece_id).color)
        cur_player.status = PlayerStatus.WAIT
        # поменять статус следующего игрока на совершение хода
        next_player = PlayerGameSessionModel.objects.get(session_id=session, color=self.get_next_colour(
            PieceModel.objects.get(id=piece_id).color))
        next_player.status = PlayerStatus.CURRENT
        # если ход невозможен, вызываем исключение

    def get_next_colour(self, cur_col):
        col_tuple = (PieceColor.WHITE, PieceColor.BLACK, PieceColor.RED)
        ind = col_tuple.index(cur_col)
        # если крайний элемент
        if ind == 2:
            return col_tuple[0]
        else:
            return col_tuple[ind + 1]
