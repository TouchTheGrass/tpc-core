from rest_framework import serializers

from app.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    scores = serializers.SlugRelatedField(
        slug_field="scores",
        read_only=True)
    wins = serializers.SlugRelatedField(
        slug_field="wins",
        read_only=True)
    loses = serializers.SlugRelatedField(
        slug_field="loses",
        read_only=True)

    class Meta:
        model = User
        fields = ["id", "name", "scores", "wins", "loses"]
