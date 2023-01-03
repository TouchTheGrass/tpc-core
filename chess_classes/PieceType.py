from enum import Enum
from Direction import Direction

class PieceType(Enum):
    PAWN=(1)
    KNIGHT=(2)
    BISHOP=(3)
    ROOK=(4)
    QUEEN=(5)
    KING=(6)
    """
    # Задает значение фрагмента
    def __init__(self, value):
        self.value = value
    """
    # возвращает массивы ходов для типов элементов
    def pawnSteps(self):
        return [[Direction.FORWARD], [Direction.FORWARD, Direction.FORWARD],\
                [Direction.FORWARD, Direction.LEFT], [Direction.LEFT, Direction.FORWARD], \
                [Direction.FORWARD, Direction.RIGHT], [Direction.RIGHT, Direction.FORWARD]]

    def  knightSteps(self):
        return [[Direction.FORWARD,Direction.FORWARD,Direction.LEFT],\
    [Direction.FORWARD,Direction.FORWARD,Direction.RIGHT],\
    [Direction.FORWARD,Direction.LEFT,Direction.LEFT],\
    [Direction.FORWARD,Direction.RIGHT,Direction.RIGHT],\
    [Direction.BACKWARD,Direction.BACKWARD,Direction.LEFT],\
    [Direction.BACKWARD,Direction.BACKWARD,Direction.RIGHT],
    [Direction.BACKWARD,Direction.LEFT,Direction.LEFT],\
    [Direction.BACKWARD,Direction.RIGHT,Direction.RIGHT],\
    [Direction.LEFT,Direction.LEFT,Direction.FORWARD],\
    [Direction.LEFT,Direction.LEFT,Direction.BACKWARD],\
    [Direction.LEFT,Direction.FORWARD,Direction.FORWARD],\
    [Direction.LEFT,Direction.BACKWARD,Direction.BACKWARD],\
    [Direction.RIGHT,Direction.RIGHT,Direction.FORWARD],\
    [Direction.RIGHT,Direction.RIGHT,Direction.BACKWARD],\
    [Direction.RIGHT,Direction.FORWARD,Direction.FORWARD],\
    [Direction.RIGHT,Direction.BACKWARD,Direction.BACKWARD]]

    def bishopSteps(self):
        return [[Direction.FORWARD,Direction.LEFT],\
                [Direction.FORWARD,Direction.RIGHT],\
                [Direction.LEFT,Direction.FORWARD],\
                [Direction.RIGHT,Direction.FORWARD],\
                [Direction.BACKWARD,Direction.LEFT],\
                [Direction.BACKWARD,Direction.RIGHT],\
                [Direction.LEFT,Direction.BACKWARD],\
                [Direction.RIGHT,Direction.BACKWARD]]

    def rookSteps(self):
        return [[Direction.FORWARD],[Direction.BACKWARD],\
                [Direction.LEFT],[Direction.RIGHT]]

    def kingSteps(self):
        return [[Direction.FORWARD, Direction.LEFT],\
                [Direction.FORWARD, Direction.RIGHT],\
                [Direction.LEFT, Direction.FORWARD], \
                [Direction.RIGHT, Direction.FORWARD],\
                [Direction.BACKWARD, Direction.LEFT],\
                [Direction.BACKWARD, Direction.RIGHT],\
                [Direction.LEFT, Direction.BACKWARD],\
                [Direction.RIGHT, Direction.BACKWARD],\
                [Direction.FORWARD], [Direction.BACKWARD],\
                [Direction.LEFT], [Direction.RIGHT]]

    # Возвращает значение фрагмента
    def getValue(self):
        return self.value

    """
    Возвращает массив шагов, которые могут выполнять законные ходы.
    Ладьи, слоны и ферзи могут повторять один тип шага за ход.
    Все остальные фигуры могут делать только один шаг за ход.
    возвращает массив или массивы направлений, где каждый внутренний 
    массив является допустимым шагом
    """
    def getSteps(self):
        if self==PieceType.ROOK:
            return self.rookSteps()
        elif self==PieceType.KNIGHT:
            return self.knightSteps()
        elif self==PieceType.BISHOP:
            return self.bishopSteps()
        elif self==PieceType.PAWN:
            return self.pawnSteps()
        else:
            # У королей и королев одни и те же шаги, но королевы могут повторить один шаг.
            return self.kingSteps()

    """
    Возвращает количество разрешенных повторений шага.
    Ладьи, слоны и ферзи могут повторять один тип шага за ход.
    Все остальные фигуры могут делать только один шаг за ход.
    возвращает разрешенное количество повторений.
    """

    def getStepReps(self):
        if self==PieceType.ROOK: return 8
        elif self==PieceType.QUEEN: return 8
        elif self==PieceType.BISHOP: return 8
        else: return 1 # Короли, пешки и кони не могут повторить свои ходы.

    """
    Возвращает символ юникода, соответствующий
    черной версии этого фрагмента.
    """
    def getChar(self):
            if self==self.KING: return '\u265A'
            elif self==self.QUEEN: return '\u265B'
            elif self==self.ROOK: return '\u265C'
            elif self==self.BISHOP: return '\u265D'
            elif self==self.KNIGHT: return '\u265E'
            elif self==self.PAWN: return '\u265F'
            else: return '?'

#PR=PieceType.QUEEN
#print(PR)
#rint(PR.getSteps())
#print(PR.getStepReps())
#print(PR.getChar())
#print(PR.getValue())

