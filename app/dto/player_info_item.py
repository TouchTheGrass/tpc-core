from dataclasses import dataclass
from ..models.enumerations.player_status import PlayerStatus

@dataclass
class PlayerInfoItem:
    id: int
    status: PlayerStatus
