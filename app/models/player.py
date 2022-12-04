from django.db import models

from app.models.game_session import GameSessionModel
from app.models.player_game_session import PlayerGameSessionModel


class PlayerModel(models.Model):
    name = models.TextField()
    sessions = models.ManyToManyField(
        GameSessionModel,
        through=PlayerGameSessionModel)
