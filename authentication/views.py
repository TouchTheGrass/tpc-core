from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, LoginSerializer, InformationSerializer


class RegistrationAPIView(APIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InformationAPIView(APIView):
    serializer_class = InformationSerializer

    def get(self, request):
        model = get_user_model()
        try:
            userdata = model.objects.get(username=request.user)
            serializer = self.serializer_class(userdata)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except model.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
