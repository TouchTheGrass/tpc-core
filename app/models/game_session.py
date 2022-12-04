from django.db import models
from django.db.models import JSONField

from app.models.enumerations.game_session_status import GameSessionStatus


class GameSessionModel(models.Model):
    status = models.TextField(choices=GameSessionStatus.choices)
    rules = JSONField()
