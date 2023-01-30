from rest_framework import serializers

from app.models import User


class UserRatingItemSerializer(serializers.ModelSerializer):
    scores = serializers.SlugRelatedField(
        read_only=True,
        slug_field="scores")

    class Meta:
        model = User
        fields = ["id", "name", "scores"]


class UserRatingListSerializer(serializers.Serializer):
    list = UserRatingItemSerializer(
        many=True,
        read_only=True)

    class Meta:
        fields = ["list"]
