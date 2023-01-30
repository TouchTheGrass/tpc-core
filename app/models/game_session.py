from django.db import models

from app.models import User
from app.models.enumerations.game_session_status import GameSessionStatus
from app.models.user_game_session import UserGameSessionModel


class GameSessionModel(models.Model):
    status = models.TextField(choices=GameSessionStatus.choices)
    users = models.ManyToManyField(
        User,
        through=UserGameSessionModel)
