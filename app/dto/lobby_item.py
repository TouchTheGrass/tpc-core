from dataclasses import dataclass

@dataclass
class LobbyItem:
    game_session_id: int
    players: list 
