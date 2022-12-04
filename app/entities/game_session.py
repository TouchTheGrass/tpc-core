from dataclasses import dataclass

from app.models.enumerations.game_session_status import GameSessionStatus


@dataclass
class GameSessionEntity:
    status: GameSessionStatus
    rules: dict
    id: int = 0
