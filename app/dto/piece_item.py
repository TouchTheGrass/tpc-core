from dataclasses import dataclass


@dataclass
class PieceItem:
    id: int
    type: str
    color: str
    position: str
