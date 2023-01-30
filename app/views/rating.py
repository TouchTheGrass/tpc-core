from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from app.models import User
from app.serializers.rating import UserRatingItemSerializer


class RatingView(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserRatingItemSerializer

    @action(detail=False, methods=["get"])
    def user_rating_list(self, request):
        serializer = self.get_serializer(User.objects.all(), many=True)
        return Response(serializer.data)
