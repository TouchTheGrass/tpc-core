from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=400)
    email = serializers.CharField(max_length=400, write_only=True)
    password = serializers.CharField(max_length=400)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        model = get_user_model()
        return model.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=400)
    email = serializers.CharField(max_length=400, read_only=True)
    password = serializers.CharField(max_length=400, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username is None:
            raise serializers.ValidationError('A username is required.')
        if password is None:
            raise serializers.ValidationError('A password is required.')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this username and password was not found.')

        return {'username': user.username, 'email': user.email, 'password': user.password}


class InformationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=400, read_only=True)
    email = serializers.CharField(max_length=400, read_only=True)
    password = serializers.CharField(max_length=400, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
