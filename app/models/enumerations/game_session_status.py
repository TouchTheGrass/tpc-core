from django.db import models
from django.utils.translation import gettext_lazy as _


class GameSessionStatus(models.TextChoices):
    WAIT = _("wait")
    GAME = _("game")
    COMPLETED = _("completed")
