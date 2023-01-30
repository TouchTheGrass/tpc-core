from dataclasses import dataclass
from ..models.enumerations.game_session_status import GameSessionStatus


@dataclass
class GameSession:
    id: int
    status: str
