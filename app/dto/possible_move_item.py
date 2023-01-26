from dataclasses import dataclass
from ..models.enumerations.position import Position

@dataclass
class PossibleMoveItem:
    value: Position
