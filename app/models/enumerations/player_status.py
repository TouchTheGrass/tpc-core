from django.db import models
from django.utils.translation import gettext_lazy as _

class PlayerStatus(models.TextChoices):
    WAIT_TURN = _("wait_turn")
    CURRENT_TURN = _("current_turn")
    LOSE = _("lose")
    WIN = _("win")

