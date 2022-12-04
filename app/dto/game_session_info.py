from dataclasses import dataclass

from app.entities.game_session import GameSessionEntity
from app.models.enumerations.piece_color import PieceColor
from app.models.enumerations.player_status import PlayerStatus


@dataclass
class GameSessionInfo:
    session: GameSessionEntity
    status: PlayerStatus
    color: PieceColor
