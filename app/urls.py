from django.urls import path

from app.views.login import LoginView
from app.views.rating import RatingView
from app.views.registration import RegistrationView
from app.views.user import UserInfoView

urlpatterns = [
    path("register", RegistrationView.as_view()),
    path("login", LoginView.as_view()),
    path("rating", RatingView.as_view()),
    path("user/info", UserInfoView.as_view()),
]
