from enum import Enum

from app.services.chess_classes.direction import Direction

class PieceType(Enum):
    PAWN=("pawn")
    KNIGHT=("knight")
    BISHOP=("bishop")
    ROOK=("rook")
    QUEEN=("queen")
    KING=("king")

    def pawn_steps(self):
        """
        Возвращает массивы ходов для пешек
        """
        return [[Direction.FORWARD], [Direction.FORWARD, Direction.FORWARD],
                [Direction.FORWARD, Direction.LEFT], [Direction.LEFT, Direction.FORWARD],
                [Direction.FORWARD, Direction.RIGHT], [Direction.RIGHT, Direction.FORWARD]]

    def knight_steps(self):
        """
        Возвращает массивы ходов для коней
        """
        return [[Direction.FORWARD, Direction.FORWARD, Direction.LEFT],
                [Direction.FORWARD, Direction.FORWARD, Direction.RIGHT],
                [Direction.FORWARD, Direction.LEFT, Direction.LEFT],
                [Direction.FORWARD, Direction.RIGHT, Direction.RIGHT],
                [Direction.BACKWARD, Direction.BACKWARD, Direction.LEFT],
                [Direction.BACKWARD, Direction.BACKWARD, Direction.RIGHT],
                [Direction.BACKWARD, Direction.LEFT, Direction.LEFT],
                [Direction.BACKWARD, Direction.RIGHT, Direction.RIGHT],
                [Direction.LEFT, Direction.LEFT, Direction.FORWARD],
                [Direction.LEFT, Direction.LEFT, Direction.BACKWARD],
                [Direction.LEFT, Direction.FORWARD, Direction.FORWARD],
                [Direction.LEFT, Direction.BACKWARD, Direction.BACKWARD],
                [Direction.RIGHT, Direction.RIGHT, Direction.FORWARD],
                [Direction.RIGHT, Direction.RIGHT, Direction.BACKWARD],
                [Direction.RIGHT, Direction.FORWARD, Direction.FORWARD],
                [Direction.RIGHT, Direction.BACKWARD, Direction.BACKWARD]]

    def bishop_steps(self):
        """
        Возвращает массивы ходов для слонов
        """
        return [[Direction.FORWARD, Direction.LEFT],
                [Direction.FORWARD, Direction.RIGHT],
                [Direction.LEFT, Direction.FORWARD],
                [Direction.RIGHT, Direction.FORWARD],
                [Direction.BACKWARD, Direction.LEFT],
                [Direction.BACKWARD, Direction.RIGHT],
                [Direction.LEFT, Direction.BACKWARD],
                [Direction.RIGHT, Direction.BACKWARD]]

    def rook_steps(self):
        """
        Возвращает массивы ходов для ладей
        """
        return [[Direction.FORWARD], [Direction.BACKWARD],
                [Direction.LEFT], [Direction.RIGHT]]

    def king_steps(self):
        """
        Возвращает массивы ходов для короля
        """
        return [[Direction.FORWARD, Direction.LEFT],
                [Direction.FORWARD, Direction.RIGHT],
                [Direction.LEFT, Direction.FORWARD],
                [Direction.RIGHT, Direction.FORWARD],
                [Direction.BACKWARD, Direction.LEFT],
                [Direction.BACKWARD, Direction.RIGHT],
                [Direction.LEFT, Direction.BACKWARD],
                [Direction.RIGHT, Direction.BACKWARD],
                [Direction.FORWARD], [Direction.BACKWARD],
                [Direction.LEFT], [Direction.RIGHT]]

    def get_value(self):
        """
        Возвращает значение фрагмента
        """
        return self.value

    def get_steps(self):
        """
        Возвращает массив шагов, которые могут выполнять законные ходы.
        Ладьи, слоны и ферзи могут повторять один тип шага за ход.
        Все остальные фигуры могут делать только один шаг за ход.
        Возвращает массив или массивы направлений, где каждый внутренний
        массив является допустимым шагом
        """
        if self == PieceType.ROOK:
            return self.rook_steps()
        elif self == PieceType.KNIGHT:
            return self.knight_steps()
        elif self == PieceType.BISHOP:
            return self.bishop_steps()
        elif self == PieceType.PAWN:
            return self.pawn_steps()
        else:
            # У королей и королев одни и те же шаги, но королевы могут повторить один шаг.
            return self.king_steps()

    def get_step_reps(self):
        """
        Возвращает количество разрешенных повторений шага.
        Ладьи, слоны и ферзи могут повторять один тип шага за ход.
        Все остальные фигуры могут делать только один шаг за ход.
        Возвращает разрешенное количество повторений.
        """
        if self == PieceType.ROOK:
            return 8
        elif self == PieceType.QUEEN:
            return 8
        elif self == PieceType.BISHOP:
            return 8
        else:
            return 1  # Короли, пешки и кони не могут повторить свои ходы.
