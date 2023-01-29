from enum import Enum


class Direction(Enum):
    """
    Перечисление прямолинейных направлений
    используется в качестве основы для всех ходов.
    """
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
