from typing import List
from app.services.chess_classes.Board import Board
from app.models.piece import PieceModel
from app.models.piece import GameSessionModel
from app.models.player_game_session import PlayerGameSessionModel
from app.models.enumerations.player_status import PlayerStatus
from app.models.enumerations.piece_type import PieceType
from utilites import board_list_forming

class EngineService:


    def get_possible_moves(self,session_id: int, piece_id: int) -> List[str]:
        # получим список фигур игровой сессии
        pieces_list = games[session_id].pieces
        for obj in pieces_list:
            if obj.id==piece_id:
                piece_position=obj.position
        # переводим объекты из объектов Piece в формат для работы доски [[piece type, piece colour, position], ... ]
        pieces_list=board_list_forming(pieces_list)
        # создаем доску для игры
        board = Board(pieces_list)
        possible_moves=board.display_legal_moves_for_engine(piece_position)
        return possible_moves


    def move_piece(self, session_id: int,piece_id: int, position: str):
        # получим список фигур игровой сессии
        pieces_list = games[session_id].pieces
        for obj in pieces_list:
            if obj.id == piece_id:
                # получаем объект фигуры
                piece_obj=obj
                # получаем позицию фигуры
                piece_position = obj.position
                # получим цвет фигуры
                piece_color=obj.color
        # переводим объекты из объектов Piece в формат для работы доски [[piece type, piece colour, position], ... ]
        pieces_list = board_list_forming(pieces_list)
        # создаем доску для игры
        board=Board(pieces_list)
        # делаем ход на созданной доске
        res=board.make_move(piece_position, position)
        # съеденных фигур и особых операций в виде повышения пешки и рокировки нет, если len(res)=0
        if len(res)==0:
            # изменим значение position у фигуры
            piece_obj.position=position
        # res - список данных для изменения БД
        # съедение фигуры
        elif len(res)==1:
            # изменим значение position у фигуры
            piece_obj.position = position
            # получим съеденную объект съеденной фигуры и удалим его
            for obj in pieces_list:
                if obj.color==res[0].get_colour().value[1] and obj.type==res[0].get_type().value:
                    del obj
            # добавление очков за съеденные фигуры
            self.adding_points(session_id, piece_color, res[0].get_type())
            # если съеден король, поменять статус игры
            if res[0].get_type()==PieceType.KING:
                # player_info status становится win и lose
                players_list=games[session_id].players
                for obj in players_list:
                    if obj.status==PlayerStatus("current_turn"):
                        obj.status=PlayerStatus("win")
                    else:
                        obj.status = PlayerStatus("lose")

                # user_game_session active становится False
                user_game_session_list=UserGameSessionModel.objects.filter(game_session_id=session_id, active=True)
                for obj in user_game_session_list:
                    obj.active=False
                    obj.status = UserStatus("disconnected")
                    # если цвет текущего игрока соответствует цвету UserGameSessionModel
                    if obj.color==piece_color:
                        obj.is_winner=True
                        obj.scores+=50
                    else:
                        obj.is_winner=False
                    scores_table = UserScoresModel.objects.get(user_id=obj.user_id)
                    scores_table.scores += obj.scores

                # session status -completed
                game_session_obj=GameSessionModel.objects.filter(id=session_id)
                game_session_obj.status=SessionStatus("completed")

        # рокировка и повышение пешки еще в процессе
        # рокировка
        elif len(res)==2:
            # изменение position для короля
            king_piece=PieceModel.objects.get(id=piece_id)
            king_piece.position = position
            # изменим position для ладьи
            rook_piece=PieceModel.objects.get(game_session=session, type=res[0].get_type().name, color=res[0].get_colour().name)
            start_rook_pos=rook_piece.position
            rook_piece.position=res[1]
            # записать ход ладьи в историю
            #self.write_session_motion(rook_piece.id, start_rook_pos, rook_piece.position)

        # повышение пешки
        elif len(res)==3:
            # меняем тип фигуры на QUEEN
            pawn_piece=PieceModel.objects.get(id=piece_id)
            pawn_piece.type=PieceType.QUEEN
        # Записать ход в историю
        #self.write_session_motion(piece_id,start_position, position)
        # поменять статус игрока данной сессии из текущего цвета на ожидание
        cur_player=PlayerGameSessionModel.objects.get(session_id=session, color=PieceModel.objects.get(id=piece_id).color)
        cur_player.status=PlayerStatus.WAIT
        # поменять статус следующего игрока на совершение хода
        next_player=PlayerGameSessionModel.objects.get(session_id=session, color=self.get_next_colour(PieceModel.objects.get(id=piece_id).color))
        next_player.status=PlayerStatus.CURRENT
        # если ход невозможен, вызываем исключение

        

    def adding_points(self, session_id, cur_color, eaten_piece_type):
        user_game_session_list = UserGameSessionModel.objects.filter(game_session_id=session_id, active=True)
        for obj in user_game_session_list:
            if obj.color == cur_color:
                if eaten_piece_type==PieceType.ROOK or eaten_piece_type==PieceType.BISHOP or eaten_piece_type==PieceType.KNIGHT:
                    obj.scores+=10
                elif eaten_piece_type==PieceType.PAWN:
                    obj.scores+=1
                elif eaten_piece_type==PieceType.QUEEN:
                    obj.scores+=25

