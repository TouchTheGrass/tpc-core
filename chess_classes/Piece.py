"""
Определенная фигура на доске.
Каждая имеет цвет и тип
и является неизменяемой.
Не является перечислением, поэтому у нас могут быть одинаковые,
но неравные фигуры, такие как пешки.
"""
class Piece:
    """
    Создает фигуру заданного типа и цвета.
    параметр type- тип элемента
    параметр colour - цвет изделия
    """
    def __init__(self, type, colour):
        self.type = type
        self.colour = colour

    # возвращает тип фигуры
    def getType(self):

        return self.type

    # возвращает значение фигуры
    def getValue(self):
        return self.type.getValue()

    # возвращает цвет фигуры
    def getColour(self):

        return self.colour

    # возвращает строковое представление фигуры
    def toString(self):
        return self.colour.toString() + " " + self.type.toString()
