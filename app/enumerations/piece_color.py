from django.db import models
from django.utils.translation import gettext_lazy as _


class PieceColor(models.TextChoices):
    WHITE = _("white")
    BLACK = _("black")
    RED = _("red")
