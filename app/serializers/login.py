from django.contrib.auth import authenticate
from rest_framework import serializers

from app.models import User


class LoginSerializer(serializers.ModelSerializer[User]):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["email", "username", "password", "tokens"]

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])
        return {
            "access": user.tokens["access"],
            "refresh": user.tokens["refresh"]
        }

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("A user with this email and password was not found")

        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens
        }
