from django.urls import path
from ..app.consumers.consumers import Interaction_With_The_Lobby
from ..app.consumers.consumers import LobbyListWebsocket

websocket_urlpatterns = [
    path('/lobby/info', Interaction_With_The_Lobby.as_asgi()),
    path('/lobby/list',LobbyListWebsocket.as_asgi())
]

