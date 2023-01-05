from django.db import models
from django.utils.translation import gettext_lazy as _


class PieceType(models.TextChoices):
    KING = _("king")
    QUEEN = _("queen")
    ROOK = _("rook")
    BISHOP = _("bishop")
    KNIGHT = _("knight")
    PAWN = _("pawn")