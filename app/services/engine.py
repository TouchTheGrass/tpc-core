from typing import List

from app.entities.game_session import GameSessionEntity
from app.entities.piece import PieceEntity
from app.models.enumerations.game_session_status import GameSessionStatus


class EngineService:

    def create_game_session(self) -> GameSessionEntity:
        # TODO
        raise NotImplementedError

    def get_game_session_status(self) -> GameSessionStatus:
        # TODO
        raise NotImplementedError

    def get_pieces(self) -> List[PieceEntity]:
        # TODO
        raise NotImplementedError

    def get_possible_moves(self, piece_id: int) -> List[str]:
        # TODO
        raise NotImplementedError

    def move_piece(self, piece_id: int, position: str) -> List[PieceEntity]:
        # TODO
        raise NotImplementedError
