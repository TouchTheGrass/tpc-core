class Piece:
    """
    Определенная фигура на доске.
    Каждая имеет цвет и тип и является неизменяемой.
    Не является перечислением, поэтому у нас могут быть одинаковые,
    но неравные фигуры, такие как пешки.
    """
    def __init__(self, type, colour):
        """
        Создает фигуру заданного типа и цвета.

        :param type: Тип фигуры
        :param colour: Цвет фигуры
        """
        self.type = type
        self.colour = colour

    def get_type(self):
        """ Возвращает тип фигуры """
        return self.type

    def get_color(self):
        """ Возвращает цвет фигуры """
        return self.colour
