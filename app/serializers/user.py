from rest_framework import serializers

from app.models import User, UserGameSession


class UserInfoSerializer(serializers.ModelSerializer):
    scores = serializers.IntegerField(source='user_scores.scores')
    wins = serializers.SerializerMethodField()
    loses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "scores", "wins", "loses"]

    def get_wins(self, instance):
        return instance.user_game_sessions.filter(is_winner=True).count()

    def get_loses(self, instance):
        return instance.user_game_sessions.filter(is_winner=False).count()


class UserHistoryItemSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField()

    class Meta:
        model = UserGameSession
        fields = ["id", "scores", "players"]

    def get_players(self, instance):
        return instance.game_session.users.values_list("username", flat=True)
