from typing import List

from app.entities.game_session import GameSessionEntity


class GameSessionDAO:

    def find_all(self) -> List[GameSessionEntity]:
        # TODO
        raise NotImplementedError

    def find_by_id(self, game_session_id: int) -> GameSessionEntity:
        # TODO
        raise NotImplementedError

    def save(self, game_session: GameSessionEntity) -> GameSessionEntity:
        # TODO
        raise NotImplementedError

    def update(self, initial: GameSessionEntity, updated: GameSessionEntity):
        # TODO
        raise NotImplementedError

    def delete(self, game_session: GameSessionEntity):
        # TODO
        raise NotImplementedError
