from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from app.enumerations.piece_type import PieceType
from app.managers.user import UserManager
from app.enumerations.game_session_status import GameSessionStatus
from app.enumerations.piece_color import PieceColor
from app.enumerations.player_status import PlayerStatus


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
        db_table = "user"

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class UserScores(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="scores")
    scores = models.IntegerField()

    class Meta:
        db_table = "user_scores"


class GameSession(models.Model):
    status = models.TextField(choices=GameSessionStatus.choices)
    users = models.ManyToManyField("User", through="UserGameSession", related_name='game_sessions')

    class Meta:
        db_table = "game_session"


class UserGameSession(models.Model):
    game_session = models.ForeignKey("GameSession", on_delete=models.CASCADE, related_name='user_game_sessions')
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='user_game_sessions')
    active = models.BooleanField()
    status = models.TextField(choices=PlayerStatus.choices)
    color = models.TextField(choices=PieceColor.choices)
    is_winner = models.BooleanField()
    scores = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_game_session"


class PieceModel(models.Model):
    type = models.TextField(choices=PieceType.choices)
    color = models.TextField(choices=PieceColor.choices)
    position = models.CharField(max_length=4)
    game_session = models.ForeignKey(
        GameSession,
        on_delete=models.CASCADE)
