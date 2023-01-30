from django.db import models

from app.models import User


class UserScores(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True)
    scores = models.IntegerField()
