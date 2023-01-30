from rest_framework import serializers

from app.models import User


class UserRatingItemSerializer(serializers.ModelSerializer):
    scores = serializers.IntegerField(source='user_scores.scores')

    class Meta:
        model = User
        fields = ["id", "username", "scores"]
