from dataclasses import dataclass
from ..models.enumerations.piece_type import PieceType
from ..models.enumerations.position import Position

@dataclass
class PieceMove:
    id: int
    position:Position
