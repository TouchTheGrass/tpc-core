from PieceType import PieceType
from Direction import Direction
from Colour import Colour
from Position import Position
from Piece import Piece
import ImpossiblePositionException
"""
Основной класс для представления состояния игры.
 * Доска сопоставляет каждую позицию с фигурой в этой позиции,
* или null свободен. Он также записывает предыдущие ходы
*, а также чей это ход и какие фигуры были
 * захвачен каким игроком.
"""

class Board:

    def __init__(self):
        self.gameOver=False
        self.board = {}
        for c in list(Colour):
            self.board[Position.get(c, 0, 2)] = Piece(PieceType.BISHOP, c)
            self.board[Position.get(c, 0, 5)] = Piece(PieceType.BISHOP, c)
            self.board[Position.get(c, 0, 0)] = Piece(PieceType.ROOK, c)
            self.board[Position.get(c, 0, 7)] = Piece(PieceType.ROOK, c)
            self.board[Position.get(c, 0, 1)] = Piece(PieceType.KNIGHT, c)
            self.board[Position.get(c, 0, 6)] = Piece(PieceType.KNIGHT, c)

            self.board[Position.get(c, 0, 3)] = Piece(PieceType.QUEEN, c)
            self.board[Position.get(c, 0, 4)] = Piece(PieceType.KING, c)
            for i in range(0, 8):
                self.board[Position.get(c, 1, i)] = Piece(PieceType.PAWN, c)
                self.board[Position.get(c,2,i)]=None
                self.board[Position.get(c, 3, i)] = None

    """
    # positions - массив [[piece type, piece colour, position], ... ]
    def __init__(self, positions):
        self.board={}

        for i in range(len(positions)):
            c=Colour(positions[i][1])
            self.board[Position(positions[i][2])]= Piece(PieceType(positions[i][0]), c)


    
     Выполняет один шаг хода, такой как L-образный ход коня или диагональный шаг слона.
     Ладьи, слоны и ферзи могут повторять один шаг несколько раз, но все остальные фигуры могут перемещаться только на один шаг за ход.
     Обратите внимание, что цвет фигуры имеет значение, поскольку движение вперед за 4-й ряд фактически означает движение назад относительно доски.
     Он не проверяет, является ли перемещение законным или возможным.
     param piece перемещаемый фрагмент
     param step массив последовательности направлений на шаге
     param current начальное положение шага.
     верните позицию в конце шага.
     выдает исключение ImpossiblePositionException, если шаг убирает фигуру с доски.
    
    def step(self, piece, step, current):
        reverse = False
        for d in step:
            if (piece.getColour() != current.getColour() and piece.getType() == PieceType.PAWN) or reverse: # reverse directions for knights

                if d.name=="FORWARD": d.name = Direction.BACKWARD.name

                elif d.name=="BACKWARD": d.name = Direction.FORWARD.name

                elif d.name=="LEFT": d.name = Direction.RIGHT.name

                elif d.name=="RIGHT": d.name = Direction.LEFT.name

            next = current.neighbour(d)
            if (next.getColour() != current.getColour()):
                reverse = True
            current = next

        return current

    """
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
            if (piece.getColour()!=current.getColour() and piece.getType() == PieceType.PAWN)\
                    or reverse:
                  if d== Direction.FORWARD: d = Direction.BACKWARD
                  elif d==Direction.BACKWARD: d = Direction.FORWARD
                  elif d==Direction.LEFT: d = Direction.RIGHT
                  elif d==Direction.RIGHT: d = Direction.LEFT
            next = current.neighbour(d)
            # need to reverse directions when switching between sections of the board
            if(next.getColour()!= current.getColour()):
                reverse=True
            current = next
        return current


    """
    Возвращает фигуру заданного положения.
    @param position положение элемента,
    @верните фигуру этой позиции или null, если позиция свободна.
    """
    def getPiece(self, position):
        if position in self.board:
            return self.board[position]
        else:
            return None

    def getPosition(self, piece_type, piece_colour):
        reverseBoard = dict(map(reversed, self.board.items()))
        for el in reverseBoard.keys():
            if el != None:
                if el.getType()==piece_type and el.getColour()==piece_colour:
                    return reverseBoard.get(el)

    def all_positions_of_colour(self, colour):
        pos_list=[]
        reverseBoard = dict(map(reversed, self.board.items()))
        for el in reverseBoard.keys():
            if el != None:
                if el.getColour() == colour:
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
    def isLegalMove(self, start, fin):
        mover = self.getPiece(start)
        target = self.getPiece(fin)
        #print(str(mover.getColour().name)+" "+str(mover.getType().name))
        #print(str(target.getColour().name) + " " + str(target.getType().name))
        # Brd.move(Position.WA2, Position.WA3)
        if (mover == None): return False
        mCol = mover.getColour()
        if (target != None and mCol == target.getColour()): return False
        steps = mover.getType().getSteps()

        if mover.getType()==PieceType.PAWN:
            for i in range(len(steps)):
                try:
                    if (fin == self.step(mover, steps[i], start) \
                            and ((target == None and i == 0) \
                    or (target == None and i == 1 and start.getColour() == mCol and start.getRow() == 1 \
                    and self.board[Position.get(mCol, 2, start.getColumn())] == None) \
                    or (target != None and i > 1))):
                            return True
                except: ImpossiblePositionException

        elif mover.getType()==PieceType.KNIGHT:
            for i in range(len(steps)):
                try:
                    if (fin == self.step(mover, steps[i], start)):
                        return True
                except: ImpossiblePositionException

        elif mover.getType()==PieceType.KING:
            for i in range(len(steps)):
                try:
                    if (fin == self.step(mover, steps[i], start)): return True
                except: ImpossiblePositionException
            try:
                if (start == Position.get(mCol, 0, 4)):
                    if (fin == Position.get(mCol, 0, 6)):
                        castle = self.board[Position.get(mCol, 0, 7)]
                        empty1 = self.board[Position.get(mCol, 0, 5)]
                        empty2 = self.board[Position.get(mCol, 0, 6)]
                        if (castle != None and castle.getType() == PieceType.ROOK \
                                and castle.getColour() == mover.getColour() \
                                and empty1 == None and empty2 == None):
                                    return True

                    if (fin == Position.get(mCol, 0, 2)):
                        castle = self.board[Position.get(mCol, 0, 0)]
                        empty1 = self.board[Position.get(mCol, 0, 1)]
                        empty2 = self.board[Position.get(mCol, 0, 2)]
                        empty3 = self.board[Position.get(mCol, 0, 3)]
                        if (castle != None and castle.getType() == PieceType.ROOK \
                                and castle.getColour() == mover.getColour() \
                                and empty1 == None and empty2 == None and empty3 == None):
                                    return True
            except: ImpossiblePositionException
        else: # rook, bishop, queen, just need to check that one of their steps is iterated.
            for i in range(len(steps)):
                step = steps[i]
                try:
                    tmp = self.step(mover, step, start)
                    while (fin != tmp and self.board[tmp] == None):
                        tmp = self.step(mover, step, tmp, tmp.getColour() != start.getColour())

                    if (fin == tmp): return True
                except: ImpossiblePositionException

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
        if (self.isLegalMove(start, fin)):

            mover = self.board[start]
            # если клетка пуста, такого значения в словаре нет -> будет ошибка KeyError
            taken = self.board[fin]
            #self.board.pop(start)
            self.board[start]=None
            if (mover.getType() == PieceType.PAWN and fin.getRow() == 0 and fin.getColour() != mover.getColour()):
                self.board[fin]= Piece(PieceType.QUEEN, mover.getColour())
            else: self.board[fin]= mover
            if (mover.getType() == PieceType.KING and start.getColumn() == 4 and start.getRow() == 0):
                if (fin.getColumn() == 2):
                    rookPos = Position[mover.getColour(), 0, 0]
                    self.board[Position.get(mover.getColour(),0,3)]= self.board[rookPos]
                    self.board.pop(rookPos)
                elif (fin.getColumn() == 6):
                    rookPos = Position.get(mover.getColour(), 0, 7)
                    self.board[Position.get(mover.getColour(), 0, 5)]= self.board[rookPos]
                    self.board.pop(rookPos)

            if (taken != None):
                # ??? добавить очки игроку
                if (taken.getType() == PieceType.KING): self.gameOver=True

        else:
            print("Illegal Move: " + str(start.name) +"-" + str(fin.name))
            #raise ImpossiblePositionException("Illegal Move: "+str(start.name)+"-"+str(end.name))

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
    #def move(self, start, end):
    #    self.move(start, end, 0)

    # возвращает список возможных ходов
    def displayLegalMoves(self, pos):
        legal_moves=[]
        for el in list(Position):
            if self.isLegalMove(pos,el):
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
            piece_moves=self.displayLegalMoves(el)
            if piece_moves!=None:
                for i in piece_moves:
                    legal_moves.append(i)
        return legal_moves

    def all_legal_moves_of_pieces(self, for_colour):
        legal_moves=[]
        # получим все положения фигур цвета for_colour
        for el in self.all_positions_of_colour(for_colour):
            # добавляем возможные ходы всех фигур определенного цвета
            piece_moves=self.displayLegalMoves(el)
            if piece_moves!=None:
                for i in piece_moves:
                    legal_moves.extend([[i,el]])
        # возвращает список [[доступный ход, позиция фигуры ],[..]]
        return legal_moves

    # есть ли возможность съесть угрожающую фигуру
    def ability_to_eat(self, target_pos, enem_moves, my_moves):
        attack_piece=[]
        for el in enem_moves:
            if el[0]==target_pos:
                # позиции угрожающих фигур
                attack_piece.append(el[1])
        # если позиция атакующей фигуры входит в список возможных ходов цвета
        if attack_piece in my_moves:
            return True
        else:
            return False


    def check_check_and_checkmate (self, for_colour):# проверка шаха и мата
        # позиция короля
        position_of_king = self.getPosition(PieceType.KING, for_colour)
        # возможные ходы вражеских фигур
        enem_moves = self.enemy_moves(for_colour)
        my_moves = self.all_legal_moves(for_colour)
        # проходимся по списку доступных ходов
        king_moves = self.displayLegalMoves(position_of_king)
        # проверяет находится ли король на возможных ходах противника
        # если да, то шах, если нет, нет шаха
        # если да и королю некуда идти И никто не может съесть угрожающую фигуру, то мат
        # return 0- ни шах, и не мат
        # return 1- шах
        # return 2- мат
        if position_of_king in enem_moves:
            # если королю некуда идти и нет возможности съесть угрожающую фигуру
            if king_moves==None and self.ability_to_eat==False:
                return 2
            return 1
        else:
            return 0


    def enemy_moves(self, for_colour):
        enemy_moves=[]
        for c in list(Colour):  # проверка угрозы от всех вражеских цветов
            if c != for_colour:
                for i in self.all_legal_moves_of_pieces(c):
                    enemy_moves.append(i)
        return enemy_moves

    # проверка закончена ли игра
    def is_it_end_game(self):
        return self.gameOver

    # функция переставления фигуры с помощью введения начальной и конечной координаты строкового формата 'A8'
    def make_move(self, start, end):
        coords = {
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
        start=coords.get(start)
        end=coords.get(end)
        self.move(start, end)


Brd=Board()
#print(str(Brd.getPiece(Position.WF1).getColour())+" "+str(Brd.getPiece(Position.WF1).getType()))
#Brd.move(Position.WE2, Position.WE4)
#Brd.make_move('L7', 'L6')
print(Brd.is_it_end_game())
Brd.move(Position.WF2, Position.WF4)
Brd.move(Position.WF4, Position.RC4)
Brd.move(Position.RC4, Position.RC3)
Brd.move(Position.RC3, Position.RD2)
Brd.move(Position.RD2, Position.RE1)
print(Brd.is_it_end_game())








