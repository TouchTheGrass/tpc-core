from dataclasses import dataclass

from django.db import models

from app.dto.game_session_info import GameSessionInfo


@dataclass
class PlayerEntity(models.Model):
    name: str
    active_game_session: GameSessionInfo
    id: int = 0
