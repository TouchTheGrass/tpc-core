from django.db import models

from app.models.enumerations.piece_color import PieceColor
from app.models.enumerations.player_status import PlayerStatus


class PlayerGameSessionModel(models.Model):
    is_active: models.BooleanField()
    status: models.TextField(choices=PlayerStatus.choices)
    color: models.TextField(choices=PieceColor.choices)
