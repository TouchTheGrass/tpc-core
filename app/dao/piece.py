from typing import List

from app.entities.piece import PieceEntity


class PieceDAO:

    def find_all(self) -> List[PieceEntity]:
        # TODO
        raise NotImplementedError

    def find_by_id(self, piece_id: int) -> PieceEntity:
        # TODO
        raise NotImplementedError

    def find_by_game_session_id(self, game_session_id: int) -> List[PieceEntity]:
        # TODO
        raise NotImplementedError

    def save(self, piece: PieceEntity) -> PieceEntity:
        # TODO
        raise NotImplementedError

    def update(self, initial: PieceEntity, updated: PieceEntity):
        # TODO
        raise NotImplementedError

    def delete(self, piece: PieceEntity):
        # TODO
        raise NotImplementedError
