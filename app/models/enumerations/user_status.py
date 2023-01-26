from django.db import models
from django.utils.translation import gettext_lazy as _


class UserStatus(models.TextChoices):
    CONNECTING = _("connecting")
    NOT_READY = _("not_ready")
    READY = _("ready")
    PLAYING = _("playing")
    DONE = _("done")
    DISCONNECTED = _("disconnected")
