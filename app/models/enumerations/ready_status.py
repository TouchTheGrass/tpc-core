from django.db import models
from django.utils.translation import gettext_lazy as _


class ReadyStatus(models.TextChoices):
    NOT_READY = _("not_ready")
    READY = _("ready")