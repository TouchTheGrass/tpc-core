from django.urls import path

from .views import RegistrationAPIView, LoginAPIView, InformationAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('info/', InformationAPIView.as_view(), name='info'),
]
