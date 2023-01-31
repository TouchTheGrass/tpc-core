from django.urls import path
from app.consumers import InteractionWithTheLobby
from app.consumers import LobbyListWebsocket

websocket_urlpatterns = [
    path("lobby/info", InteractionWithTheLobby.as_asgi()),
    path("lobby/list", LobbyListWebsocket.as_asgi())
]
