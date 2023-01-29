from enum import Enum
from app.models.enumerations.piece_color import PieceColor
from app.services.chess_classes.impossible_position_exception import ImpossiblePositionException


class Position(Enum):
    """
    Перечисление 96 позиций на доске
    Каждая позиция имеет свойство цвет, ряд (0-3) и колонка (0-7)
    """

    # Белая часть доски
    WA1 = (PieceColor.WHITE, 0, 0)
    WA2 = (PieceColor.WHITE, 1, 0)
    WA3 = (PieceColor.WHITE, 2, 0)
    WA4 = (PieceColor.WHITE, 3, 0)
    WB1 = (PieceColor.WHITE, 0, 1)
    WB2 = (PieceColor.WHITE, 1, 1)
    WB3 = (PieceColor.WHITE, 2, 1)
    WB4 = (PieceColor.WHITE, 3, 1)
    WC1 = (PieceColor.WHITE, 0, 2)
    WC2 = (PieceColor.WHITE, 1, 2)
    WC3 = (PieceColor.WHITE, 2, 2)
    WC4 = (PieceColor.WHITE, 3, 2)
    WD1 = (PieceColor.WHITE, 0, 3)
    WD2 = (PieceColor.WHITE, 1, 3)
    WD3 = (PieceColor.WHITE, 2, 3)
    WD4 = (PieceColor.WHITE, 3, 3)
    WE1 = (PieceColor.WHITE, 0, 4)
    WE2 = (PieceColor.WHITE, 1, 4)
    WE3 = (PieceColor.WHITE, 2, 4)
    WE4 = (PieceColor.WHITE, 3, 4)
    WF1 = (PieceColor.WHITE, 0, 5)
    WF2 = (PieceColor.WHITE, 1, 5)
    WF3 = (PieceColor.WHITE, 2, 5)
    WF4 = (PieceColor.WHITE, 3, 5)
    WG1 = (PieceColor.WHITE, 0, 6)
    WG2 = (PieceColor.WHITE, 1, 6)
    WG3 = (PieceColor.WHITE, 2, 6)
    WG4 = (PieceColor.WHITE, 3, 6)
    WH1 = (PieceColor.WHITE, 0, 7)
    WH2 = (PieceColor.WHITE, 1, 7)
    WH3 = (PieceColor.WHITE, 2, 7)
    WH4 = (PieceColor.WHITE, 3, 7)

    # Черная часть доски
    BA1 = (PieceColor.BLACK, 0, 0)
    BA2 = (PieceColor.BLACK, 1, 0)
    BA3 = (PieceColor.BLACK, 2, 0)
    BA4 = (PieceColor.BLACK, 3, 0)
    BB1 = (PieceColor.BLACK, 0, 1)
    BB2 = (PieceColor.BLACK, 1, 1)
    BB3 = (PieceColor.BLACK, 2, 1)
    BB4 = (PieceColor.BLACK, 3, 1)
    BC1 = (PieceColor.BLACK, 0, 2)
    BC2 = (PieceColor.BLACK, 1, 2)
    BC3 = (PieceColor.BLACK, 2, 2)
    BC4 = (PieceColor.BLACK, 3, 2)
    BD1 = (PieceColor.BLACK, 0, 3)
    BD2 = (PieceColor.BLACK, 1, 3)
    BD3 = (PieceColor.BLACK, 2, 3)
    BD4 = (PieceColor.BLACK, 3, 3)
    BE1 = (PieceColor.BLACK, 0, 4)
    BE2 = (PieceColor.BLACK, 1, 4)
    BE3 = (PieceColor.BLACK, 2, 4)
    BE4 = (PieceColor.BLACK, 3, 4)
    BF1 = (PieceColor.BLACK, 0, 5)
    BF2 = (PieceColor.BLACK, 1, 5)
    BF3 = (PieceColor.BLACK, 2, 5)
    BF4 = (PieceColor.BLACK, 3, 5)
    BG1 = (PieceColor.BLACK, 0, 6)
    BG2 = (PieceColor.BLACK, 1, 6)
    BG3 = (PieceColor.BLACK, 2, 6)
    BG4 = (PieceColor.BLACK, 3, 6)
    BH1 = (PieceColor.BLACK, 0, 7)
    BH2 = (PieceColor.BLACK, 1, 7)
    BH3 = (PieceColor.BLACK, 2, 7)
    BH4 = (PieceColor.BLACK, 3, 7)

    # Красная часть доски
    RA1 = (PieceColor.RED, 0, 0)
    RA2 = (PieceColor.RED, 1, 0)
    RA3 = (PieceColor.RED, 2, 0)
    RA4 = (PieceColor.RED, 3, 0)
    RB1 = (PieceColor.RED, 0, 1)
    RB2 = (PieceColor.RED, 1, 1)
    RB3 = (PieceColor.RED, 2, 1)
    RB4 = (PieceColor.RED, 3, 1)
    RC1 = (PieceColor.RED, 0, 2)
    RC2 = (PieceColor.RED, 1, 2)
    RC3 = (PieceColor.RED, 2, 2)
    RC4 = (PieceColor.RED, 3, 2)
    RD1 = (PieceColor.RED, 0, 3)
    RD2 = (PieceColor.RED, 1, 3)
    RD3 = (PieceColor.RED, 2, 3)
    RD4 = (PieceColor.RED, 3, 3)
    RE1 = (PieceColor.RED, 0, 4)
    RE2 = (PieceColor.RED, 1, 4)
    RE3 = (PieceColor.RED, 2, 4)
    RE4 = (PieceColor.RED, 3, 4)
    RF1 = (PieceColor.RED, 0, 5)
    RF2 = (PieceColor.RED, 1, 5)
    RF3 = (PieceColor.RED, 2, 5)
    RF4 = (PieceColor.RED, 3, 5)
    RG1 = (PieceColor.RED, 0, 6)
    RG2 = (PieceColor.RED, 1, 6)
    RG3 = (PieceColor.RED, 2, 6)
    RG4 = (PieceColor.RED, 3, 6)
    RH1 = (PieceColor.RED, 0, 7)
    RH2 = (PieceColor.RED, 1, 7)
    RH3 = (PieceColor.RED, 2, 7)
    RH4 = (PieceColor.RED, 3, 7)

    def __init__(self, color, row, column):
        """
        Создаем позицию с указанным цветом, строкой и столбцом
        :param color: Цвет участка доски, в котором позиция.
        :param row: Номер строки (0-3) позиции.
        :param column: Номер столбца (0-7) позиции.
        """
        self.color = color
        self.row = row
        self.column = column

    def get_color(self):
        """
        Возвращает цвет позиции
        """
        return self.color

    def get_row(self):
        """
        Возвращает строку позиции
        """
        return self.row

    def get_column(self):
        """
        Возвращает столбец позиции
        """
        return self.column

    @staticmethod
    def get(color, row, column):
        """
        Получим позицию, соответствующую указанному цвету, строке и столбцу.

        :return: Положение указанного цвета, строки и столбца.
        :raises ImpossiblePositionException: Если это выходит за пределы доски.
        """
        index = row + 4 * column
        if 0 <= index < 32:
            if color.name == "WHITE":
                return list(Position)[index]
            elif color.name == "BLACK":
                return list(Position)[index + 32]
            elif color.name == "RED":
                return list(Position)[index + 64]
        else:
            raise ImpossiblePositionException("No such position.")

    def neighbour(self, direction):
        """
        Получает соседнюю ячейку в заданном направлении.
        Ячейки всегда перемещаются вперед к центральной линии,
        таким образом, направление не зависит от цвета изделия.

        :return: Положение в указанном направлении.
        :raises ImpossiblePositionException: При движении назад от задней шеренги или перемещение с боковой части доски.
        """
        if direction.name == "FORWARD":
            if self.row < 3:
                return self.get(self.color, self.row + 1, self.column)
            if self.column < 4:
                return self.get(list(PieceColor)[(int(self.color.value) + 1) % 3], 3, 7 - self.column)
            return self.get(list(PieceColor)[(int(self.color.value) + 2) % 3], 3, 7 - self.column)
        elif direction.name == "BACKWARD":
            if self.row == 0:
                raise ImpossiblePositionException("Moved off board")
            return self.get(self.color, self.row - 1, self.column)
        elif direction.name == "LEFT":
            if self.column == 0:
                raise ImpossiblePositionException("Moved off board")
            return self.get(self.color, self.row, self.column - 1)
        elif direction.name == "RIGHT":
            if self.column == 7:
                raise ImpossiblePositionException("Moved off board")
            return self.get(self.color, self.row, self.column + 1)
        else:
            raise ImpossiblePositionException("Unreachable code?")

    def even_parity(self):
        """
        :return: True, если позиция имеет четный паритет; эквивалентно черному квадрату на традиционной шахматной доске.
        """
        return (self.row + self.column) % 2 == 0
