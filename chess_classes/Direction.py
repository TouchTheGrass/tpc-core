from enum import Enum

#Перечисление прямолинейных направлений
# используется в качестве основы для всех ходов.

class Direction(Enum):
    FORWARD="FORWARD"
    BACKWARD="BACKWARD"
    LEFT="LEFT"
    RIGHT="RIGHT"
