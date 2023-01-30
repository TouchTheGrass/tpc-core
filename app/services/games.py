from dataclasses import dataclass
from app.models.chess_classes.piece_type import PieceTypeEngine
from app.models.chess_classes.color import PieceColorEngine
from app.models.enumerations.player_status import PlayerStatus

@dataclass
class GameInfo:
    players: list
    pieces: list

@dataclass
class Piece:
    id: int
    game_session_id: int
    type: PieceTypeEngine
    color:PieceColorEngine
    position: str

@dataclass
class PlayerInfo:
    user_id: int
    game_session_id: int
    player_status: PlayerStatus

games={}




