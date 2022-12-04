from django.db import models
from django.utils.translation import gettext_lazy as _


class PlayerStatus(models.TextChoices):
    CONNECTING = _("connecting")
    CONNECTED = _("connected")
    WAIT = _("wait")
    CURRENT = _("current")
    ELIMINATED = _("eliminated")
    DISCONNECTED = _("disconnected")

