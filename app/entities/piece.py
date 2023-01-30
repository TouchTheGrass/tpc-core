from dataclasses import dataclass

from django.db import models

from app.models.enumerations.piece_color import PieceColor
from app.models.enumerations.piece_type import PieceType


@dataclass
class PieceEntity(models.Model):
    type: PieceType
    color: PieceColor
    position: str
    id: int = 0
