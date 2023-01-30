from django.db import models

from app.models import User
from app.models.enumerations.piece_color import PieceColor
from app.models.enumerations.player_status import PlayerStatus
from app.models.game_session import GameSessionModel


class UserGameSessionModel(models.Model):
    user: models.ForeignKey(User, on_delete=models.CASCADE)
    game_session: models.ForeignKey(GameSessionModel, on_delete=models.CASCADE)
    active: models.BooleanField()
    status: models.TextField(choices=PlayerStatus.choices)
    color: models.TextField(choices=PieceColor.choices)
    is_winner: models.BooleanField()
    scores: models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
