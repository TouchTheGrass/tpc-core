from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.serializers.user import UserInfoSerializer, UserHistoryItemSerializer


class UserInfoView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInfoSerializer

    @action(detail=True, methods=["get"])
    def info(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class UserHistoryView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserHistoryItemSerializer

    @action(detail=True, methods=["get"])
    def history(self, request):
        user = request.user
        serializer = self.get_serializer(user.user_game_sessions, many=True)
        return Response(serializer.data)
