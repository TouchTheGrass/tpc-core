from app.enumerations.piece_type import PieceType
from app.enumerations.piece_color import PieceColor
from app.services.chess_classes.direction import Direction
from app.services.chess_classes.impossible_position_exception import ImpossiblePositionException
from app.services.chess_classes.piece import Piece
from app.services.chess_classes.position import Position


class Board:
    """
    Основной класс для представления состояния игры.
    Доска сопоставляет каждую позицию с фигурой в этой позиции,
    или null свободен. Он также записывает предыдущие ходы,
    а также чей это ход и какие фигуры были
    захвачен каким игроком.
    """

    def __init__(self, positions):
        """
        :param positions: список [[piece type, piece color, position], ... ]
        """
        self.coords = {
            # white
            'A8': Position.WH1, 'B8': Position.WG1, 'C8': Position.WF1, 'D8': Position.WE1, 'I8': Position.WD1,
            'J8': Position.WC1,
            'K8': Position.WB1, 'L8': Position.WA1, 'A7': Position.WH2, 'B7': Position.WG2, 'C7': Position.WF2,
            'D7': Position.WE2,
            'I7': Position.WD2, 'J7': Position.WC2, 'K7': Position.WB2, 'L7': Position.WA2,
            'A6': Position.WH3, 'B6': Position.WG3, 'C6': Position.WF3, 'D6': Position.WE3, 'I6': Position.WD3,
            'J6': Position.WC3,
            'K6': Position.WB3, 'L6': Position.WA3,
            'A5': Position.WH4, 'B5': Position.WG4, 'C5': Position.WF4, 'D5': Position.WE4, 'I5': Position.WD4,
            'J5': Position.WC4,
            'K5': Position.WB4, 'L5': Position.WA4,

            # red
            'A1': Position.RA1, 'B1': Position.RB1, 'C1': Position.RC1, 'D1': Position.RD1, 'E1': Position.RE1,
            'F1': Position.RF1,
            'G1': Position.RG1, 'H1': Position.RH1,
            'A2': Position.RA2, 'B2': Position.RB2, 'C2': Position.RC2, 'D2': Position.RD2, 'E2': Position.RE2,
            'F2': Position.RF2,
            'G2': Position.RG2, 'H2': Position.RH2,
            'A3': Position.RA3, 'B3': Position.RB3, 'C3': Position.RC3, 'D3': Position.RD3, 'E3': Position.RE3,
            'F3': Position.RF3,
            'G3': Position.RG3, 'H3': Position.RH3,
            'A4': Position.RA4, 'B4': Position.RB4, 'C4': Position.RC4, 'D4': Position.RD4, 'E4': Position.RE4,
            'F4': Position.RF4,
            'G4': Position.RG4, 'H4': Position.RH4,

            # black
            'L12': Position.BH1, 'K12': Position.BG1, 'J12': Position.BF1, 'I12': Position.BE1, 'E12': Position.BD1,
            'F12': Position.BC1,
            'G12': Position.BB1, 'H12': Position.BA1,
            'L11': Position.BH2, 'K11': Position.BG2, 'J11': Position.BF2, 'I11': Position.BE2, 'E11': Position.BD2,
            'F11': Position.BC2,
            'G11': Position.BB2, 'H11': Position.BA2,
            'L10': Position.BH3, 'K10': Position.BG3, 'J10': Position.BF3, 'I10': Position.BE3, 'E10': Position.BD3,
            'F10': Position.BC3,
            'G10': Position.BB3, 'H10': Position.BA3,
            'L9': Position.BH4, 'K9': Position.BG4, 'J9': Position.BF4, 'I9': Position.BE4, 'E9': Position.BD4,
            'F9': Position.BC4,
            'G9': Position.BB4, 'H9': Position.BA4
        }

        # заполнить словарь координата:None
        self.board = {
            # white
            Position.WH1: None, Position.WG1: None, Position.WF1: None, Position.WE1: None, Position.WD1: None,
            Position.WC1: None,
            Position.WB1: None, Position.WA1: None, Position.WH2: None, Position.WG2: None, Position.WF2: None,
            Position.WE2: None,
            Position.WD2: None, Position.WC2: None, Position.WB2: None, Position.WA2: None,
            Position.WH3: None, Position.WG3: None, Position.WF3: None, Position.WE3: None, Position.WD3: None,
            Position.WC3: None,
            Position.WB3: None, Position.WA3: None,
            Position.WH4: None, Position.WG4: None, Position.WF4: None, Position.WE4: None, Position.WD4: None,
            Position.WC4: None,
            Position.WB4: None, Position.WA4: None,

            # red
            Position.RA1: None, Position.RB1: None, Position.RC1: None, Position.RD1: None, Position.RE1: None,
            Position.RF1: None,
            Position.RG1: None, Position.RH1: None,
            Position.RA2: None, Position.RB2: None, Position.RC2: None, Position.RD2: None, Position.RE2: None,
            Position.RF2: None,
            Position.RG2: None, Position.RH2: None,
            Position.RA3: None, Position.RB3: None, Position.RC3: None, Position.RD3: None, Position.RE3: None,
            Position.RF3: None,
            Position.RG3: None, Position.RH3: None,
            Position.RA4: None, Position.RB4: None, Position.RC4: None, Position.RD4: None, Position.RE4: None,
            Position.RF4: None,
            Position.RG4: None, Position.RH4: None,

            # black
            Position.BH1: None, Position.BG1: None, Position.BF1: None, Position.BE1: None, Position.BD1: None,
            Position.BC1: None,
            Position.BB1: None, Position.BA1: None,
            Position.BH2: None, Position.BG2: None, Position.BF2: None, Position.BE2: None, Position.BD2: None,
            Position.BC2: None,
            Position.BB2: None, Position.BA2: None,
            Position.BH3: None, Position.BG3: None, Position.BF3: None, Position.BE3: None, Position.BD3: None,
            Position.BC3: None,
            Position.BB3: None, Position.BA3: None,
            Position.BH4: None, Position.BG4: None, Position.BF4: None, Position.BE4: None, Position.BD4: None,
            Position.BC4: None,
            Position.BB4: None, Position.BA4: None}

        self.game_over = False
        for i in range(len(positions)):
            c = PieceColor(positions[i][1])
            position = self.coords.get(positions[i][2])
            # board[position]=piece_type
            self.board[Position(position)] = Piece(PieceType(positions[i][0]), c)

    def step(self, piece, step, start, reverse=False):
        """
        Выполняет один шаг хода, такой как L-образный
        ход коня или диагональный шаг слона.
        Ладьи, слоны и ферзи могут повторять один шаг несколько раз,
        но все остальные фигуры могут перемещаться только на один шаг за ход.
        Обратите внимание, что цвет фигуры имеет значение,
        поскольку движение вперед за 4-й ряд фактически означает движение назад относительно доски.
        Он не проверяет, является ли перемещение законным или возможным.
        Перегруженная операция с дополнительным параметром,
        позволяющим проверить, нужно ли отменить повторное перемещение.

        :param piece: Перемещаемая фигура
        :param step: Массив последовательности направлений на шаге
        :param start: Начальное положение шага.
        :param reverse: Следует ли менять местами шаги (если фигура пересекает секцию доски).
        :returns: Позиция фигуры в конце шага.
        :raise ImpossiblePositionException: Шаг убирает фигуру с доски.
        """

        current_step = start
        for d in step:
            if (piece.get_color() != current_step.get_color() and piece.get_type() == PieceType.PAWN) or reverse:
                if d == Direction.FORWARD:
                    d = Direction.BACKWARD
                elif d == Direction.BACKWARD:
                    d = Direction.FORWARD
                elif d == Direction.LEFT:
                    d = Direction.RIGHT
                elif d == Direction.RIGHT:
                    d = Direction.LEFT
            next_step = current_step.neighbour(d)
            # необходимость изменения направления при переключении между секциями доски
            if next_step.get_color() != current_step.get_color():
                reverse = True
            current_step = next_step
        return current_step

    def get_piece(self, position):
        """
        Возвращает фигуру заданного положения.

        :param position: Положение элемента,
        :returns: фигуру этой позиции или null, если позиция свободна.
        """
        if position in self.board:
            return self.board[position]
        else:
            return None

    def get_position(self, piece_type, piece_color):
        reverse_board = dict(map(reversed, self.board.items()))
        for el in reverse_board.keys():
            if el is not None:
                if el.get_type() == piece_type and el.get_color() == piece_color:
                    return reverse_board.get(el)

    def all_positions_of_color(self, color):
        pos_list = []
        reverse_board = dict(map(reversed, self.board.items()))
        for el in reverse_board.keys():
            if el is not None:
                if el.get_color() == color:
                    pos_list.append(reverse_board.get(el))
        return pos_list

    def is_legal_move(self, start, fin):
        """
        Проверяет, является ли перемещение законным.
        Ход определяется начальной позицией и конечной позицией.

        Проверенными условия являются:

        - в начальной позиции находится фигура;

        - цвет этой фигуры соответствует игроку, чья очередь;

        - если в конечном положении находится деталь, она не может совпадать с движущейся деталью;

        - движущаяся деталь должна выполнять один или несколько шагов, разрешенных для ее типа, включая два шага вперед для начальных ходов пешкой и рокировок влево и вправо;

        - фигуры, которые могут совершать повторяющиеся ходы, должны повторять один тип шага и не могут проходить через какую-либо другую фигуру.

        Обратите внимание, что проход запрещен, вы можете сделать замок после того, как король или ладья сделали ход,
        но они должны были вернуться на исходную позицию, все пешки, достигшие заднего ряда, повышаются до ферзя,
        вы можете сделать ход в шах, и вы можете оставить своего короля в шах, и вы можете сделать замок поперек шаха.
        """
        mover = self.get_piece(start)
        target = self.get_piece(fin)
        if mover is None:
            return False
        m_col = mover.get_color()
        if target is not None and m_col == target.get_color():
            return False
        steps = mover.get_type().get_steps()

        if mover.get_type() == PieceType.PAWN:
            for i in range(len(steps)):
                try:
                    if (fin == self.step(mover, steps[i], start)
                            and ((target is None and i == 0)
                                 or (target is None and i == 1 and start.get_color() == m_col and start.get_row() == 1
                                     and self.board[Position.get(m_col, 2, start.get_column())] is None)
                                 or (target is not None and i > 1))):
                        return True
                except Exception:
                    raise ImpossiblePositionException("Illegal move")

        elif mover.get_type() == PieceType.KNIGHT:
            for i in range(len(steps)):
                try:
                    if fin == self.step(mover, steps[i], start):
                        return True
                except Exception:
                    raise ImpossiblePositionException("Illegal move")

        elif mover.get_type() == PieceType.KING:
            for i in range(len(steps)):
                try:
                    if fin == self.step(mover, steps[i], start):
                        return True
                except Exception:
                    raise ImpossiblePositionException("Illegal move")
            try:
                if start == Position.get(m_col, 0, 4):
                    if fin == Position.get(m_col, 0, 6):
                        castle = self.board[Position.get(m_col, 0, 7)]
                        empty1 = self.board[Position.get(m_col, 0, 5)]
                        empty2 = self.board[Position.get(m_col, 0, 6)]
                        if (castle is not None and castle.get_type() == PieceType.ROOK
                                and castle.get_color() == mover.get_color()
                                and empty1 is None and empty2 is None):
                            return True

                    if fin == Position.get(m_col, 0, 2):
                        castle = self.board[Position.get(m_col, 0, 0)]
                        empty1 = self.board[Position.get(m_col, 0, 1)]
                        empty2 = self.board[Position.get(m_col, 0, 2)]
                        empty3 = self.board[Position.get(m_col, 0, 3)]
                        if (castle is not None and castle.get_type() == PieceType.ROOK
                                and castle.get_color() == mover.get_color()
                                and empty1 is None and empty2 is None and empty3 is None):
                            return True
            except Exception:
                raise ImpossiblePositionException("Illegal move")
        else:  # rook, bishop, queen, just need to check that one of their steps is iterated.
            for i in range(len(steps)):
                step = steps[i]
                try:
                    tmp = self.step(mover, step, start)
                    while fin != tmp and self.board[tmp] is None:
                        tmp = self.step(mover, step, tmp, tmp.get_color() != start.get_color())

                    if fin == tmp:
                        return True
                except Exception:
                    raise ImpossiblePositionException("Illegal move")

        return False

    def move(self, start, fin):
        """
        Выполняет законный ход. 
        Если фигура взята, она заменяется в этой позиции взятой фигурой.
        Игра заканчивается, когда забирается король.
        Когда пешка достигает заднего ранга, она автоматически повышается до ферзя.

        :param start: Начальная позиция перемещения
        :param fin: Конечная позиция перемещения
        """
        if self.is_legal_move(start, fin):

            mover = self.board[start]
            # если клетка пуста, такого значения в словаре нет -> будет ошибка KeyError
            taken = self.board[fin]
            self.board[start] = None
            if mover.get_type() == PieceType.PAWN and fin.get_row() == 0 and fin.get_color() != mover.get_color():
                self.board[fin] = Piece(PieceType.QUEEN, mover.get_color())
                # возвращает перемещаемую пешку, ее новый тип и цвет
                return [self.board[fin], PieceType.QUEEN, mover.get_color().name]
            else:
                self.board[fin] = mover

            # рокировка
            if mover.get_type() == PieceType.KING and start.get_column() == 4 and start.get_row() == 0:
                if fin.get_column() == 2:
                    rook_pos = Position.get(mover.get_color(), 0, 0)
                    self.board[Position.get(mover.get_color(), 0, 3)] = self.board[rook_pos]
                    self.board.pop(rook_pos)
                    rook_pos = {'WHITE': 'I8', 'BLACK': 'E12', 'RED': 'D1'}
                    # возвращает фигуру ладьи и позицию, куда она перемещается
                    return [self.board[Position.get(mover.get_color(), 0, 3)], rook_pos.get(mover.get_color().name)]
                elif fin.get_column() == 6:
                    rook_pos = Position.get(mover.get_color(), 0, 7)
                    self.board[Position.get(mover.get_color(), 0, 5)] = self.board[rook_pos]
                    self.board.pop(rook_pos)
                    rook_pos = {'WHITE': 'C8', 'BLACK': 'J12', 'RED': 'F1'}
                    # возвращает фигуру ладьи и позицию, куда она перемещается
                    return [self.board[Position.get(mover.get_color(), 0, 5)], rook_pos.get(mover.get_color().name)]

            if taken is not None:
                # если фигуру съедают
                if taken is not None:
                    if taken.get_type() == PieceType.KING:
                        self.game_over = True
                    return [taken]
            return []
        else:
            raise ImpossiblePositionException("Illegal Move: " + str(start.name) + "-" + str(fin.name))

    def display_legal_moves_for_engine(self, pos):
        """
        Возвращает список возможных ходов в формате координат для лицевой доски
        """
        legal_moves = []
        pos = self.coords.get(pos)
        for el in list(Position):
            if self.is_legal_move(pos, el):
                inv_coord = {v: k for k, v in self.coords.items()}
                el = inv_coord.get(el)
                legal_moves.append(el)

        if len(legal_moves) == 0:
            return None
        else:
            return legal_moves

    def display_legal_moves(self, pos):
        """
        Возвращает список возможных ходов
        """
        legal_moves = []
        for el in list(Position):
            if self.is_legal_move(pos, el):
                legal_moves.append(el)
        if len(legal_moves) == 0:
            return None
        else:
            return legal_moves

    def all_legal_moves(self, for_color):
        legal_moves = []
        # получим все положения фигур цвета for_color
        for el in self.all_positions_of_color(for_color):
            # добавляем возможные ходы всех фигур определенного цвета
            piece_moves = self.display_legal_moves(el)
            if piece_moves is not None:
                for i in piece_moves:
                    legal_moves.append(i)
        return legal_moves

    def all_legal_moves_of_pieces(self, for_color):
        legal_moves = []
        # получим все положения фигур цвета for_color
        for el in self.all_positions_of_color(for_color):
            # добавляем возможные ходы всех фигур определенного цвета
            piece_moves = self.display_legal_moves(el)
            if piece_moves is not None:
                for i in piece_moves:
                    legal_moves.extend([[i, el]])
        # возвращает список [[доступный ход, позиция фигуры ],[..]]
        return legal_moves

    def ability_to_eat(self, target_pos, enemy_moves, my_moves):
        """
        Есть ли возможность съесть угрожающую фигуру
        """
        attack_piece = []
        for el in enemy_moves:
            if el[0] == target_pos:
                # позиции угрожающих фигур
                attack_piece.append(el[1])
        # если позиция атакующей фигуры входит в список возможных ходов цвета и ее не прикрывают

        if self.el_in_list(attack_piece, my_moves) == 1:
            if self.try_to_make_move(target_pos, attack_piece[0]):
                return True
            else:
                return False
        else:
            return False

    def el_in_list(self, part, all):
        counter = 0
        for el in part:
            if el in all:
                counter += 1
        return counter

    def try_to_make_move(self, start, end):
        temp_board = self.board
        self.move(start, end)
        if self.is_check_and_checkmate(self.board[end].get_color()) == 1:
            self.board = temp_board
            return False
        self.board = temp_board
        return True

    def is_check_and_checkmate(self, for_color):
        """
        Проверка шаха и мата;
        проверяет, находится ли король на возможных ходах противника;
        если да, то шах, если нет, нет шаха;
        если да и королю некуда идти И никто не может съесть угрожающую фигуру, то мат.

        :returns: 1: ни шах, и не мат; 2: шах; 3: мат
        """
        # позиция короля
        position_of_king = self.get_position(PieceType.KING, for_color)
        # возможные ходы вражеских фигур
        enemy_moves_to_where_from = self.enemy_moves(for_color)
        enemy_moves = []
        for el in enemy_moves_to_where_from:
            enemy_moves.append(el[0])
        my_moves = self.all_legal_moves(for_color)
        # проходимся по списку доступных ходов
        king_moves = self.display_legal_moves(position_of_king)
        if position_of_king in enemy_moves:
            # если королю некуда идти и нет возможности съесть угрожающую фигуру
            if (self.ability_to_eat(position_of_king, enemy_moves_to_where_from, my_moves) is False
                    and self.opportunity_to_escape(king_moves, enemy_moves) is False):
                return 2
            return 1
        else:
            return 0

    def opportunity_to_escape(self, king_moves, enemy_moves):
        for el in king_moves:
            if self.board[el] is None:
                if el not in enemy_moves:
                    return True
        return False

    def enemy_moves(self, for_color):
        """
        Возможные ходы противников для фигур цвета for_color
        """
        enemy_moves = []
        for c in list(PieceColor):  # проверка угрозы от всех вражеских цветов
            if c != for_color:
                for i in self.all_legal_moves_of_pieces(c):
                    enemy_moves.append(i)
        return enemy_moves

    def is_it_end_game(self):
        """
        Проверка закончена ли игра
        """
        return self.game_over

    def make_move(self, start, end):
        """
        Функция перестановки фигуры с помощью введения начальной и конечной координаты строкового формата 'A8'
        """
        start = self.coords.get(start)
        end = self.coords.get(end)
        res = self.move(start, end)
        return res
