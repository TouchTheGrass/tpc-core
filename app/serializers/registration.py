from rest_framework import serializers

from app.models import User, UserScores


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserScores.objects.create(user_id=user.id, scores=0)
        return user
