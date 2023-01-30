from django.urls import path

from app.views.login import LoginView
from app.views.rating import RatingView
from app.views.registration import RegistrationView
from app.views.user import UserInfoView, UserHistoryView

urlpatterns = [
    path("auth/register", RegistrationView.as_view()),
    path("auth/login", LoginView.as_view()),
    path("rating", RatingView.as_view({"get": "user_rating_list"})),
    path("user/info", UserInfoView.as_view({"get": "info"})),
    path("user/history", UserHistoryView.as_view({"get": "history"})),
]
