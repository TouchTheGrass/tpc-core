from django.db import models

from app.models.enumerations.piece_color import PieceColor
from app.models.enumerations.piece_type import PieceType
from app.models.game_session import GameSessionModel


class PieceModel(models.Model):
    type = models.TextField(choices=PieceType.choices)
    color = models.TextField(choices=PieceColor.choices)
    position = models.CharField(max_length=4)
    game_session = models.ForeignKey(
        GameSessionModel,
        on_delete=models.CASCADE)
