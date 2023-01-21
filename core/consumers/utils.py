from app.models.game_session import GameSessionModel
from app.models.enumerations.game_session_status import GameSessionStatus

def get_list_of_available_lobbies():
    # доступны лобби у которых game_session status -wait
    list_of_available_lobbies = []
    waiting_game_sessions = GameSessionModel.objects.filter(status=GameSessionStatus.WAIT)
    for el in waiting_game_sessions:
        # id игровой сессии
        game_session_id = el.id
        # получаем объекты участников конкретной сессии
        users = UserGameSessionModel.objects.filter(game_sessiion_id=el.id)
        # получим id игроков
        players_id = []
        for pl in users:
            players_id.append(pl.user_id)
    return [game_session_id, [players_id]]
