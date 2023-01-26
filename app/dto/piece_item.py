from dataclasses import dataclass
from ..models.enumerations.piece_type import PieceType
from ..models.enumerations.piece_color import PieceColor
from ..models.enumerations.position import Position

@dataclass
class PieceItem:
    id: int
    type: PieceType
    color: PieceColor
    position: Position
