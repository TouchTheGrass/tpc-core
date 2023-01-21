#from app.models.enumerations.piece_type import PieceType
#from app.models.enumerations.piece_color import PieceColor
from PieceType import PieceType
from Colour import PieceColor
from Direction import Direction
from Position import Position
from Piece import Piece
from ImpossiblePositionException import ImpossiblePositionException
"""
Основной класс для представления состояния игры.
 * Доска сопоставляет каждую позицию с фигурой в этой позиции,
* или null свободен. Он также записывает предыдущие ходы
*, а также чей это ход и какие фигуры были
 * захвачен каким игроком.
"""

class Board:

    """ positions - список [[piece type, piece colour, position], ... ] """
    def __init__(self, positions):
        self.coords = {
            # white
            'A8': Position.WH1, 'B8': Position.WG1, 'C8': Position.WF1, 'D8': Position.WE1, 'I8': Position.WD1,
            'J8': Position.WC1, \
            'K8': Position.WB1, 'L8': Position.WA1, 'A7': Position.WH2, 'B7': Position.WG2, 'C7': Position.WF2,
            'D7': Position.WE2, \
            'I7': Position.WD2, 'J7': Position.WC2, 'K7': Position.WB2, 'L7': Position.WA2, \
            'A6': Position.WH3, 'B6': Position.WG3, 'C6': Position.WF3, 'D6': Position.WE3, 'I6': Position.WD3,
            'J6': Position.WC3, \
            'K6': Position.WB3, 'L6': Position.WA3, \
            'A5': Position.WH4, 'B5': Position.WG4, 'C5': Position.WF4, 'D5': Position.WE4, 'I5': Position.WD4,
            'J5': Position.WC4, \
            'K5': Position.WB4, 'L5': Position.WA4,
            # red
            'A1': Position.RA1, 'B1': Position.RB1, 'C1': Position.RC1, 'D1': Position.RD1, 'E1': Position.RE1,
            'F1': Position.RF1, \
            'G1': Position.RG1, 'H1': Position.RH1, \
            'A2': Position.RA2, 'B2': Position.RB2, 'C2': Position.RC2, 'D2': Position.RD2, 'E2': Position.RE2,
            'F2': Position.RF2, \
            'G2': Position.RG2, 'H2': Position.RH2, \
            'A3': Position.RA3, 'B3': Position.RB3, 'C3': Position.RC3, 'D3': Position.RD3, 'E3': Position.RE3,
            'F3': Position.RF3, \
            'G3': Position.RG3, 'H3': Position.RH3, \
            'A4': Position.RA4, 'B4': Position.RB4, 'C4': Position.RC4, 'D4': Position.RD4, 'E4': Position.RE4,
            'F4': Position.RF4, \
            'G4': Position.RG4, 'H4': Position.RH4, \
            # black
            'L12': Position.BH1, 'K12': Position.BG1, 'J12': Position.BF1, 'I12': Position.BE1, 'E12': Position.BD1,
            'F12': Position.BC1, \
            'G12': Position.BB1, 'H12': Position.BA1, \
            'L11': Position.BH2, 'K11': Position.BG2, 'J11': Position.BF2, 'I11': Position.BE2, 'E11': Position.BD2,
            'F11': Position.BC2, \
            'G11': Position.BB2, 'H11': Position.BA2, \
            'L10': Position.BH3, 'K10': Position.BG3, 'J10': Position.BF3, 'I10': Position.BE3, 'E10': Position.BD3,
            'F10': Position.BC3, \
            'G10': Position.BB3, 'H10': Position.BA3, \
            'L9': Position.BH4, 'K9': Position.BG4, 'J9': Position.BF4, 'I9': Position.BE4, 'E9': Position.BD4,
            'F9': Position.BC4, \
            'G9': Position.BB4, 'H9': Position.BA4
        }
        # заполнить словарь координата:None
        self.board={ # white
            Position.WH1:None, Position.WG1:None, Position.WF1:None, Position.WE1:None, Position.WD1:None,
            Position.WC1:None,
            Position.WB1:None, Position.WA1:None, Position.WH2:None, Position.WG2:None, Position.WF2:None,
            Position.WE2:None, \
            Position.WD2:None, Position.WC2:None, Position.WB2:None, Position.WA2:None, \
            Position.WH3:None, Position.WG3:None, Position.WF3:None, Position.WE3:None, Position.WD3:None,
            Position.WC3:None, \
            Position.WB3:None, Position.WA3:None, \
            Position.WH4:None, Position.WG4:None, Position.WF4:None, Position.WE4:None, Position.WD4:None,
            Position.WC4:None, \
            Position.WB4:None, Position.WA4:None,
            # red
            Position.RA1:None, Position.RB1:None, Position.RC1:None, Position.RD1:None, Position.RE1:None,
            Position.RF1:None, \
            Position.RG1:None, Position.RH1:None, \
            Position.RA2:None, Position.RB2:None, Position.RC2:None, Position.RD2:None, Position.RE2:None,
            Position.RF2:None, \
            Position.RG2:None, Position.RH2:None, \
            Position.RA3:None, Position.RB3:None, Position.RC3:None, Position.RD3:None, Position.RE3:None,
            Position.RF3:None, \
            Position.RG3:None, Position.RH3:None, \
            Position.RA4:None, Position.RB4:None, Position.RC4:None, Position.RD4:None, Position.RE4:None,
            Position.RF4:None, \
            Position.RG4:None, Position.RH4:None, \
            # black
            Position.BH1:None, Position.BG1:None, Position.BF1:None, Position.BE1:None, Position.BD1:None,
            Position.BC1:None, \
            Position.BB1:None, Position.BA1:None, \
            Position.BH2:None, Position.BG2:None, Position.BF2:None, Position.BE2:None, Position.BD2:None,
            Position.BC2:None, \
            Position.BB2:None, Position.BA2:None, \
            Position.BH3:None, Position.BG3:None, Position.BF3:None, Position.BE3:None, Position.BD3:None,
            Position.BC3:None, \
            Position.BB3:None, Position.BA3:None, \
            Position.BH4:None, Position.BG4:None, Position.BF4:None, Position.BE4:None, Position.BD4:None,
            Position.BC4:None, \
            Position.BB4:None, Position.BA4:None}

        self.gameOver=False
        for i in range(len(positions)):
            c=PieceColor(positions[i][1])
            position=self.coords.get(positions[i][2])
            # board[position]=piece_type
            self.board[Position(position)]= Piece(PieceType(positions[i][0]), c)

    """
    Выполняет один шаг хода, такой как L-образный ход коня или диагональный шаг слона.
     * Ладьи, слоны и ферзи могут повторять один шаг несколько раз, но все остальные фигуры могут перемещаться только на один шаг за ход.
     * Обратите внимание, что цвет фигуры имеет значение, поскольку движение вперед за 4-й ряд фактически означает движение назад относительно доски.
     * Он не проверяет, является ли перемещение законным или возможным.
     * Перегруженная операция с дополнительным параметром, позволяющим проверить, нужно ли отменить повторное перемещение. 
     * @param piece перемещаемый фрагмент
     * @param step массив последовательности направлений на шаге
     * @param current начальное положение шага.
     * @param reverse следует ли менять местами шаги (если фигура пересекает секцию доски).
     * @верните позицию в конце шага.
     * @выдает исключение ImpossiblePositionException, если шаг убирает фигуру с доски.
    """
    def step(self, piece, step, current, reverse=False):
        for d in step:
            if (piece.get_colour() != current.get_colour() and piece.get_type() == PieceType.PAWN)\
                    or reverse:
                  if d== Direction.FORWARD: d = Direction.BACKWARD
                  elif d==Direction.BACKWARD: d = Direction.FORWARD
                  elif d==Direction.LEFT: d = Direction.RIGHT
                  elif d==Direction.RIGHT: d = Direction.LEFT
            next = current.neighbour(d)
            # необходимость изменения направления при переключении между секциями доски
            if(next.get_colour()!= current.get_colour()):
                reverse=True
            current = next
        return current


    """
    Возвращает фигуру заданного положения.
    @param position положение элемента,
    @верните фигуру этой позиции или null, если позиция свободна.
    """
    def get_piece(self, position):
        if position in self.board:
            return self.board[position]
        else:
            return None

    def get_position(self, piece_type, piece_colour):
        reverseBoard = dict(map(reversed, self.board.items()))
        for el in reverseBoard.keys():
            if el != None:
                if el.get_type()==piece_type and el.get_colour()==piece_colour:
                    return reverseBoard.get(el)

    def all_positions_of_colour(self, colour):
        pos_list=[]
        reverseBoard = dict(map(reversed, self.board.items()))
        for el in reverseBoard.keys():
            if el != None:
                if el.get_colour() == colour:
                    pos_list.append(reverseBoard.get(el))
        return pos_list
    """
    Проверяет, является ли перемещение законным. 
     * Ход определяется начальной позицией (с которой начинается движущаяся фигура)
    * и конечной позицией, в которую фигура намеревается переместиться.
     * Проверенные условия являются: 
     * в начальной позиции находится фигура; 
     * цвет этой фигуры соответствует игроку, чья очередь;
     * если в конечном положении находится деталь, она не может совпадать с движущейся деталью;
     * движущаяся деталь должна выполнять один или несколько шагов, разрешенных для ее типа, включая
     * два шага вперед для начальных ходов пешкой и рокировок влево и вправо;
     * фигуры, которые могут совершать повторяющиеся ходы, должны повторять один тип шага и не могут проходить через какую-либо другую фигуру.
     * Обратите внимание, что проход запрещен, вы можете сделать замок после того, как король или ладья сделали ход 
     * но они должны были вернуться на исходную позицию, все пешки, достигшие заднего ряда, повышаются до ферзя,
    * вы можете сделать ход в шах, и вы можете оставить своего короля в шах, и вы можете сделать замок поперек шаха.
    """
    def is_legal_move(self, start, fin):
        mover = self.get_piece(start)
        target = self.get_piece(fin)
        if (mover == None): return False
        mCol = mover.get_colour()
        if (target != None and mCol == target.get_colour()): return False
        steps = mover.get_type().get_steps()

        if mover.get_type()==PieceType.PAWN:
            for i in range(len(steps)):
                try:
                    if (fin == self.step(mover, steps[i], start) \
                            and ((target == None and i == 0) \
                    or (target == None and i == 1 and start.get_colour() == mCol and start.get_row() == 1 \
                        and self.board[Position.get(mCol, 2, start.get_column())] == None) \
                    or (target != None and i > 1))):
                            return True
                except:
                    ImpossiblePositionException

        elif mover.get_type()==PieceType.KNIGHT:
            for i in range(len(steps)):
                try:
                    if (fin == self.step(mover, steps[i], start)):
                        return True
                except:
                    ImpossiblePositionException

        elif mover.get_type()==PieceType.KING:
            for i in range(len(steps)):
                try:
                    if (fin == self.step(mover, steps[i], start)): return True
                except:
                    ImpossiblePositionException
            try:
                if (start == Position.get(mCol, 0, 4)):
                    if (fin == Position.get(mCol, 0, 6)):
                        castle = self.board[Position.get(mCol, 0, 7)]
                        empty1 = self.board[Position.get(mCol, 0, 5)]
                        empty2 = self.board[Position.get(mCol, 0, 6)]
                        if (castle != None and castle.get_type() == PieceType.ROOK \
                                and castle.get_colour() == mover.get_colour() \
                                and empty1 == None and empty2 == None):
                                    return True

                    if (fin == Position.get(mCol, 0, 2)):
                        castle = self.board[Position.get(mCol, 0, 0)]
                        empty1 = self.board[Position.get(mCol, 0, 1)]
                        empty2 = self.board[Position.get(mCol, 0, 2)]
                        empty3 = self.board[Position.get(mCol, 0, 3)]
                        if (castle != None and castle.get_type() == PieceType.ROOK \
                                and castle.get_colour() == mover.get_colour() \
                                and empty1 == None and empty2 == None and empty3 == None):
                                    return True
            except:
                ImpossiblePositionException
        else: # rook, bishop, queen, just need to check that one of their steps is iterated.
            for i in range(len(steps)):
                step = steps[i]
                try:
                    tmp = self.step(mover, step, start)
                    while (fin != tmp and self.board[tmp] == None):
                        tmp = self.step(mover, step, tmp, tmp.get_colour() != start.get_colour())

                    if (fin == tmp): return True
                except:
                    ImpossiblePositionException

        return False

    """
    Выполняет законный ход. 
    * Если фигура взята, она заменяется в этой позиции взятой фигурой.
    * Игра заканчивается, когда забирается король. 
    * Когда пешка достигает заднего ранга, она автоматически повышается до ферзя.
    * @param запускает начальную позицию перемещения
    * @param end конечная позиция перемещения
    * @param time - количество миллисекунд, затраченных на воспроизведение хода
    * @выдает исключение ImpossiblePositionException, если перемещение не является законным
    """
    def move(self, start, fin):
        if (self.is_legal_move(start, fin)):

            mover = self.board[start]
            # если клетка пуста, такого значения в словаре нет -> будет ошибка KeyError
            taken = self.board[fin]
            self.board[start]=None
            if (mover.get_type() == PieceType.PAWN and fin.get_row() == 0 and fin.get_colour() != mover.get_colour()):
                self.board[fin]= Piece(PieceType.QUEEN, mover.get_colour())
                # возвращает перемещаемую пешку, ее новый тип и цвет
                return [self.board[fin], PieceType.QUEEN, mover.get_colour().name]
            else: self.board[fin]= mover

            # рокировка
            if (mover.get_type() == PieceType.KING and start.get_column() == 4 and start.get_row() == 0):
                if (fin.get_column() == 2):
                    rookPos = Position.get(mover.get_colour(), 0, 0)
                    self.board[Position.get(mover.get_colour(), 0, 3)]= self.board[rookPos]
                    self.board.pop(rookPos)
                    rook_pos = {'WHITE': 'I8', 'BLACK':'E12', 'RED':'D1'}
                    # возвращает фигуру ладьи и позицию, куда она перемещается
                    return [self.board[Position.get(mover.get_colour(), 0, 3)], rook_pos.get(mover.get_colour().name)]
                elif (fin.get_column() == 6):
                    rookPos = Position.get(mover.get_colour(), 0, 7)
                    self.board[Position.get(mover.get_colour(), 0, 5)]= self.board[rookPos]
                    self.board.pop(rookPos)
                    rook_pos={'WHITE':'C8', 'BLACK':'J12', 'RED':'F1'}
                    # возвращает фигуру ладьи и позицию, куда она перемещается
                    return [self.board[Position.get(mover.get_colour(), 0, 5)], rook_pos.get(mover.get_colour().name)]

            if (taken != None):
                # если фигуру съедают
                if (taken != None):
                    if (taken.get_type() == PieceType.KING):
                        self.gameOver = True
                    return [taken]
            return []
        else:
            raise ImpossiblePositionException("Illegal Move: " + str(start.name) +"-" + str(fin.name))

    """
    * Выполняет законный ход. 
     * Если фигура взята, она заменяется в этой позиции взятой фигурой.
     * Игра заканчивается, когда забирается король. 
     * Когда пешка достигает заднего ранга, она автоматически повышается до ферзя.
     * Метод перегружен, чтобы разрешить несвоевременные игры.
     * @param запускает начальную позицию перемещения
     * @param end конечная позиция перемещения
     * @выдает исключение ImpossiblePositionException, если перемещение не является законным
    """
    """ возвращает список возможных ходов в формате координат для лицевой доски """
    def display_legal_moves_for_engine(self, pos):
        legal_moves=[]
        pos=self.coords.get(pos)
        for el in list(Position):
            if self.is_legal_move(pos, el):
                inv_coord = {v: k for k, v in self.coords.items()}
                el = inv_coord.get(el)
                legal_moves.append(el)

        if len(legal_moves)==0:
            return None
        else:
            return legal_moves
     
    """ возвращает список возможных ходов """
    def display_legal_moves(self, pos):
        legal_moves=[]
        for el in list(Position):
            if self.is_legal_move(pos, el):
                legal_moves.append(el)
        if len(legal_moves)==0:
            return None
        else:
            return legal_moves

    def all_legal_moves(self, for_colour):
        legal_moves=[]
        # получим все положения фигур цвета for_colour
        for el in self.all_positions_of_colour(for_colour):
            # добавляем возможные ходы всех фигур оределенного цвета
            piece_moves=self.display_legal_moves(el)
            if piece_moves!=None:
                for i in piece_moves:
                    legal_moves.append(i)
        return legal_moves

    def all_legal_moves_of_pieces(self, for_colour):
        legal_moves=[]
        # получим все положения фигур цвета for_colour
        for el in self.all_positions_of_colour(for_colour):
            # добавляем возможные ходы всех фигур определенного цвета
            piece_moves=self.display_legal_moves(el)
            if piece_moves!=None:
                for i in piece_moves:
                    legal_moves.extend([[i,el]])
        # возвращает список [[доступный ход, позиция фигуры ],[..]]
        return legal_moves

    """ есть ли возможность съесть угрожающую фигуру """
    def ability_to_eat(self, target_pos, enem_moves, my_moves):
        attack_piece=[]
        for el in enem_moves:
            if el[0]==target_pos:
                # позиции угрожающих фигур
                attack_piece.append(el[1])
        # если позиция атакующей фигуры входит в список возможных ходов цвета и ее не прикрывают

        if self.el_in_list(attack_piece,my_moves)==1:
            if self.try_to_make_move(target_pos, attack_piece[0])==True:
                return True
            else: return False
        else:
            return False

    def el_in_list(self,part, all):
        counter = 0
        for el in part:
            if el in all:
                counter += 1
        return counter


    def try_to_make_move(self, start, end):
        temp_board=self.board
        res=self.move(start, end)
        if self.check_check_and_checkmate(self.board[end].get_colour())==1:
            self.board=temp_board
            return False
        self.board = temp_board
        return True



    """ 
    Проверка шаха и мата 
    # проверяет находится ли король на возможных ходах противника
    # если да, то шах, если нет, нет шаха
    # если да и королю некуда идти И никто не может съесть угрожающую фигуру, то мат
    # return 0- ни шах, и не мат
    # return 1- шах
    # return 2- мат
    """
    def check_check_and_checkmate (self, for_colour):
        # позиция короля
        position_of_king = self.get_position(PieceType.KING, for_colour)
        # возможные ходы вражеских фигур
        enem_moves_to_wherefrom = self.enemy_moves(for_colour)
        enem_moves=[]
        for el in enem_moves_to_wherefrom:
            enem_moves.append(el[0])
        my_moves = self.all_legal_moves(for_colour)
        # проходимся по списку доступных ходов
        king_moves = self.display_legal_moves(position_of_king)
        # проверяет находится ли король на возможных ходах противника
        # если да, то шах, если нет, нет шаха
        # если да и королю некуда идти И никто не может съесть угрожающую фигуру, то мат
        # return 0- ни шах, и не мат
        # return 1- шах
        # return 2- мат

        if position_of_king in enem_moves:
            # если королю некуда идти и нет возможности съесть угрожающую фигуру
            if self.ability_to_eat(position_of_king, enem_moves_to_wherefrom, my_moves)==False and self.opportunity_to_escape(king_moves,enem_moves)==False:
                return 2
            return 1
        else:
            return 0

    def opportunity_to_escape(self,  king_moves, enem_moves):
        for el in king_moves:
            if self.board[el]==None:
                if el not in enem_moves:
                        return True
        return False
    """
    Возможные ходы противников для фигур цвета for_colour
    """
    def enemy_moves(self, for_colour):
        enemy_moves=[]
        for c in list(PieceColor):  # проверка угрозы от всех вражеских цветов
            if c != for_colour:
                for i in self.all_legal_moves_of_pieces(c):
                    enemy_moves.append(i)
        return enemy_moves

    """ Проверка закончена ли игра """
    def is_it_end_game(self):
        return self.gameOver

    """ Функция переставления фигуры с помощью введения начальной и конечной координаты строкового формата 'A8' """
    def make_move(self, start, end):
        start = self.coords.get(start)
        end = self.coords.get(end)
        res=self.move(start, end)
        return res





