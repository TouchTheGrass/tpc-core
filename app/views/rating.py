from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import User
from app.serializers.rating import UserRatingListSerializer


class RatingView(APIView):
    permission_classes = (AllowAny,)

    def get(self):
        users = User.objects.all()
        serializer = UserRatingListSerializer(data=users)
        return Response(serializer.data)
