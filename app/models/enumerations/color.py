from django.db import models
from django.utils.translation import gettext_lazy as _


class Color(models.TextChoices):
    WHITE = _("white")
    BLACK = _("black")
    RED = _("red")
    NONE= _("none")
