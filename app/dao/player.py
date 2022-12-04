from typing import List

from app.entities.player import PlayerEntity


class PlayerDAO:

    def find_all(self) -> List[PlayerEntity]:
        # TODO
        raise NotImplementedError

    def find_by_id(self, player_id: int) -> PlayerEntity:
        # TODO
        raise NotImplementedError

    def find_by_game_session_id(self, game_session_id: int) -> List[PlayerEntity]:
        # TODO
        raise NotImplementedError

    def save(self, player: PlayerEntity) -> PlayerEntity:
        # TODO
        raise NotImplementedError

    def update(self, initial: PlayerEntity, updated: PlayerEntity):
        # TODO
        raise NotImplementedError

    def delete(self, player: PlayerEntity):
        # TODO
        raise NotImplementedError
