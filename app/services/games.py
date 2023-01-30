from dataclasses import dataclass
from app.models.enumerations.piece_type import PieceType
from app.models.enumerations.piece_color import PieceColor
from app.models.enumerations.player_status import PlayerStatus

@dataclass
class GameInfo:
    players: list
    pieces: list

@dataclass
class Piece:
    id: int
    game_session_id: int
    type: PieceType
    color:PieceColor
    position: str

@dataclass
class PlayerInfo:
    user_id: int
    game_session_id: int
    player_status: PlayerStatus

games={}




