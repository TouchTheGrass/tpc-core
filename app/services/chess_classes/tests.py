import unittest

from Board import Board
from color import PieceColorEngine
from impossible_position_exception import ImpossiblePositionException
from piece_type import PieceTypeEngine

pos_base = [[PieceTypeEngine.QUEEN, PieceColorEngine.WHITE, 'I8'], [PieceTypeEngine.KING, PieceColorEngine.WHITE, 'D8'],
            [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'A8'], [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'L8'],
            [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'J8'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'C8'],
            [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'B8'], [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'K8'],
            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'A7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'B7'],
            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'C7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'D7'],
            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'I7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'J7'],
            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'K7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'L7'],
            [PieceTypeEngine.QUEEN, PieceColorEngine.BLACK, 'E12'], [PieceTypeEngine.KING, PieceColorEngine.BLACK, 'I12'],
            [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'H12'], [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'L12'],
            [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'F12'], [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'J12'],
            [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'G12'], [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'K12'],
            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'L11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'K11'],
            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'J11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'I11'],
            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'E11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'F11'],
            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'G11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'H11'],

            [PieceTypeEngine.QUEEN, PieceColorEngine.RED, 'D1'], [PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'],
            [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'A1'], [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'H1'],
            [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'C1'], [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'F1'],
            [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'B1'], [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'G1'],
            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'A2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'B2'],
            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'C2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'D2'],
            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'E2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'F2'],
            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'G2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'H2']
            ]
pos_for_test_PAWN_move = [[PieceTypeEngine.QUEEN, PieceColorEngine.WHITE, 'I8'], [PieceTypeEngine.KING, PieceColorEngine.WHITE, 'D8'],
                          [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'A8'], [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'L8'],
                          [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'J8'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'C8'],
                          [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'B8'], [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'K8'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'A7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'B7'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'C7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'D3'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'I7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'J7'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'K7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'L7'],

                          [PieceTypeEngine.QUEEN, PieceColorEngine.BLACK, 'E12'], [PieceTypeEngine.KING, PieceColorEngine.BLACK, 'I12'],
                          [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'H12'], [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'L12'],
                          [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'F12'], [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'J12'],
                          [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'G12'], [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'K12'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'L11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'K11'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'J11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'I9'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'E9'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'F11'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'G11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'H11'],

                          [PieceTypeEngine.QUEEN, PieceColorEngine.RED, 'D1'], [PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'],
                          [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'A1'], [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'H1'],
                          [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'C1'], [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'F1'],
                          [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'B1'], [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'G1'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'A2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'B2'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'C2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'D2'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'E4'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'F2'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'G2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'H2']
                          ]
pos_for_test_KNIGHT_move = [[PieceTypeEngine.QUEEN, PieceColorEngine.WHITE, 'I8'], [PieceTypeEngine.KING, PieceColorEngine.WHITE, 'D8'],
                            [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'A8'], [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'L8'],
                            [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'J8'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'C8'],
                            [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'B8'], [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'K8'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'A7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'B7'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'C7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'D7'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'I7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'J7'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'K7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'L7'],
                            [PieceTypeEngine.QUEEN, PieceColorEngine.BLACK, 'E12'], [PieceTypeEngine.KING, PieceColorEngine.BLACK, 'I12'],
                            [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'H12'], [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'L12'],
                            [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'F12'], [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'J12'],
                            [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'G12'], [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'K12'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'L11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'K11'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'J11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'I11'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'E11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'F11'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'G11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'H11'],

                            [PieceTypeEngine.QUEEN, PieceColorEngine.RED, 'D1'], [PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'],
                            [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'A1'], [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'H1'],
                            [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'C1'], [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'F1'],
                            [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'B1'], [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'G9'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'A2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'B2'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'C2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'D2'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'E2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'F2'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'G2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'H2']
                            ]
pos_for_test_BISHOP_move = [[PieceTypeEngine.QUEEN, PieceColorEngine.WHITE, 'I8'], [PieceTypeEngine.KING, PieceColorEngine.WHITE, 'D8'],
                            [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'A8'], [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'L8'],
                            [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'J8'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'C8'],
                            [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'B8'], [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'K8'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'A7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'B7'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'C7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'D7'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'I7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'J7'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'K7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'L7'],
                            [PieceTypeEngine.QUEEN, PieceColorEngine.BLACK, 'E12'], [PieceTypeEngine.KING, PieceColorEngine.BLACK, 'I12'],
                            [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'H12'], [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'L12'],
                            [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'F12'], [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'J12'],
                            [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'G12'], [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'K12'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'L11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'K11'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'J11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'I11'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'E11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'F11'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'G11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'H11'],

                            [PieceTypeEngine.QUEEN, PieceColorEngine.RED, 'D1'], [PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'],
                            [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'A1'], [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'H1'],
                            [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'C5'], [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'F1'],
                            [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'B1'], [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'G1'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'A2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'B2'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'C2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'D2'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'E2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'F2'],
                            [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'G2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'H2']
                            ]
pos_for_test_ROOK_move = [[PieceTypeEngine.QUEEN, PieceColorEngine.WHITE, 'I8'], [PieceTypeEngine.KING, PieceColorEngine.WHITE, 'D8'],
                          [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'A8'], [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'L8'],
                          [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'J8'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'C8'],
                          [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'B8'], [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'K8'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'A7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'B7'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'C7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'D7'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'I7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'J7'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'K7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'L7'],
                          [PieceTypeEngine.QUEEN, PieceColorEngine.BLACK, 'E12'], [PieceTypeEngine.KING, PieceColorEngine.BLACK, 'I12'],
                          [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'H12'], [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'L12'],
                          [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'F12'], [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'J12'],
                          [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'G12'], [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'K12'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'L11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'K11'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'J11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'I11'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'E11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'F11'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'G11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'H11'],

                          [PieceTypeEngine.QUEEN, PieceColorEngine.RED, 'D1'], [PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'],
                          [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'D4'], [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'H1'],
                          [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'C1'], [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'F1'],
                          [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'B1'], [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'G1'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'A2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'B2'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'C2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'D2'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'E2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'F2'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'G2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'H2']
                          ]
pos_for_test_QUEEN_move = [[PieceTypeEngine.QUEEN, PieceColorEngine.WHITE, 'I8'], [PieceTypeEngine.KING, PieceColorEngine.WHITE, 'D8'],
                           [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'A8'], [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'L8'],
                           [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'J8'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'C8'],
                           [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'B8'], [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'K8'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'A7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'B7'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'C7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'D7'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'I7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'J7'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'K7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'L7'],
                           [PieceTypeEngine.QUEEN, PieceColorEngine.BLACK, 'E12'], [PieceTypeEngine.KING, PieceColorEngine.BLACK, 'I12'],
                           [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'H12'], [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'L12'],
                           [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'F12'], [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'J12'],
                           [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'G12'], [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'K12'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'L11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'K11'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'J11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'I11'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'E11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'F11'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'G11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'H11'],

                           [PieceTypeEngine.QUEEN, PieceColorEngine.RED, 'D4'], [PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'],
                           [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'A1'], [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'H1'],
                           [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'C1'], [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'F1'],
                           [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'B1'], [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'G1'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'A2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'B2'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'C2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'D2'],
                           [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'E2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'F2'],
                           ]
pos_for_test_KING_move = [[PieceTypeEngine.QUEEN, PieceColorEngine.WHITE, 'I8'], [PieceTypeEngine.KING, PieceColorEngine.WHITE, 'D6'],
                          [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'A8'], [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'L8'],
                          [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'J8'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'C8'],
                          [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'B8'], [PieceTypeEngine.KNIGHT, PieceColorEngine.WHITE, 'K8'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'A7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'B7'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'C7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'D7'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'I7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'J7'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'K7'], [PieceTypeEngine.PAWN, PieceColorEngine.WHITE, 'L7'],
                          [PieceTypeEngine.QUEEN, PieceColorEngine.BLACK, 'E12'], [PieceTypeEngine.KING, PieceColorEngine.BLACK, 'I12'],
                          [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'H12'], [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'L12'],
                          [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'F12'], [PieceTypeEngine.BISHOP, PieceColorEngine.BLACK, 'J12'],
                          [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'G12'], [PieceTypeEngine.KNIGHT, PieceColorEngine.BLACK, 'K12'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'L11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'K11'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'J11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'I11'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'E11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'F11'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'G11'], [PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'H11'],

                          [PieceTypeEngine.QUEEN, PieceColorEngine.RED, 'D1'], [PieceTypeEngine.KING, PieceColorEngine.RED, 'D6'],
                          [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'A1'], [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'H1'],
                          [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'C1'], [PieceTypeEngine.BISHOP, PieceColorEngine.RED, 'F1'],
                          [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'B1'], [PieceTypeEngine.KNIGHT, PieceColorEngine.RED, 'G1'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'A2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'B2'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'C2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'D2'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'E2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'F2'],
                          [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'G2'], [PieceTypeEngine.PAWN, PieceColorEngine.RED, 'H2']
                          ]
pos_for_test_castling = [
    [PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'],
    [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'A1'], [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'H1'],
]
pos_test_upgrade_pawn = [[PieceTypeEngine.PAWN, PieceColorEngine.BLACK, 'F2']]
pos_test_check = [[PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'G3']]
pos_check_and_checkmate = [[PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'H3'],
                           [PieceTypeEngine.QUEEN, PieceColorEngine.WHITE, 'C2'], [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'E4']]
pos_check_ability_to_eat = [[PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'H3'],
                            [PieceTypeEngine.QUEEN, PieceColorEngine.WHITE, 'D2'], [PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'E4']]
# дамку прикрывает ладья
pos_check_ability_to_eat2 = [[PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'H3'],
                             [PieceTypeEngine.QUEEN, PieceColorEngine.WHITE, 'D2'], [PieceTypeEngine.ROOK, PieceColorEngine.BLACK, 'D3']]

pos_check_legal_moves= [[PieceTypeEngine.ROOK, PieceColorEngine.RED, 'E2'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'H3']]
pos_check_legal_moves_for_check= [[PieceTypeEngine.ROOK, PieceColorEngine.WHITE, 'E4'], [PieceTypeEngine.BISHOP, PieceColorEngine.WHITE, 'H3'],
                        [PieceTypeEngine.KING, PieceColorEngine.RED, 'E1'], [PieceTypeEngine.ROOK, PieceColorEngine.RED, 'D1']]

cells = ['A8', 'B8', 'C8', 'D8', 'I8', 'J8', 'K8', 'L8', 'A7', 'B7', 'C7', 'D7', 'I7', 'J7', 'K7', 'L7', 'A6',
         'B6', 'C6', 'D6', 'I6', 'J6', 'K6', 'L6', 'A5', 'B5', 'C5', 'D5', 'I5', 'J5', 'K5', 'L5', 'A1',
         'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'A3', 'B3',
         'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'L12', 'K12',
         'J12', 'I12', 'E12', 'F12', 'G12', 'H12', 'L11', 'K11', 'J11', 'I11', 'E11', 'F11', 'G11', 'H11',
         'L10', 'K10', 'J10', 'I10', 'E10', 'F10', 'G10', 'H10', 'L9', 'K9', 'J9', 'I9', 'E9', 'F9', 'G9', 'H9']


class TestChessEngine(unittest.TestCase):
    def setUp(self):
        self.chess_engine = Board(pos_base)

    def test_PAWN_move(self):
        # пешка из начального положения не может идти никуда кроме 2х и 1го ходов прямо
        allowed_moves = ['A3', 'A4']
        for el in cells:

            self.setUp()
            if el not in allowed_moves:
                self.assertRaises(ImpossiblePositionException, self.chess_engine.make_move, 'A2', el)
            else:
                self.assertEqual(self.chess_engine.make_move('A2', el), [])
        # ходы пешки из центальной координаты E4
        # и вражеская пешка на I9, на E9 и на D3
        allowed_moves = []
        eat_moves = ['I9']
        for el in cells:
            # self.setUp(pos1)
            self.chess_engine = Board(pos_for_test_PAWN_move)
            if el not in (allowed_moves + eat_moves):
                self.assertRaises(ImpossiblePositionException, self.chess_engine.make_move, 'E4', el)
            elif el in allowed_moves:
                self.assertEqual(self.chess_engine.make_move('E4', el), [])
            elif el in eat_moves:
                self.assertEqual([self.chess_engine.make_move('E4', el)[0].get_type()], [PieceTypeEngine.PAWN])

    def test_KNIGHT_move(self):
        allowed_moves = ['A3', 'C3']
        for el in cells:
            # self.setUp(pos_base)
            self.chess_engine = Board(pos_base)
            if el not in allowed_moves:
                self.assertRaises(ImpossiblePositionException, self.chess_engine.make_move, 'B1', el)
            else:
                self.assertEqual(self.chess_engine.make_move('B1', el), [])
        # переставим коня на G9
        allowed_moves = ['F3', 'H3', 'E10', 'E4']  #
        eat_moves = ['F11', 'H11']
        for el in cells:

            # self.setUp(pos2)
            self.chess_engine = Board(pos_for_test_KNIGHT_move)
            if el not in (allowed_moves + eat_moves):

                self.assertRaises(ImpossiblePositionException, self.chess_engine.make_move, 'G9', el)
            elif el in allowed_moves:
                self.assertEqual(self.chess_engine.make_move('G9', el), [])
            elif el in eat_moves:
                self.assertEqual([self.chess_engine.make_move('G9', el)[0].get_type()], [PieceTypeEngine.PAWN])

    def test_BISHOP_move(self):
        # поставим офицера на С5
        allowed_moves = ['B4', 'B6', 'D6', 'D4', 'A3', 'E3']  #
        eat_moves = ['A7', 'I7']  #
        for el in cells:
            # self.setUp(pos2)
            self.chess_engine = Board(pos_for_test_BISHOP_move)
            if el not in (allowed_moves + eat_moves):
                self.assertRaises(ImpossiblePositionException, self.chess_engine.make_move, 'C5', el)
            elif el in allowed_moves:
                self.assertEqual(self.chess_engine.make_move('C5', el), [])
            elif el in eat_moves:
                self.assertEqual([self.chess_engine.make_move('C5', el)[0].get_type()], [PieceTypeEngine.PAWN])

    def test_ROOK_move(self):
        # поставим ладью на D4
        allowed_moves = ['A4', 'B4', 'C4', 'D3', 'E4', 'F4', 'G4', 'H4', 'D5', 'D6']  #
        eat_moves = ['D7']
        for el in cells:
            # self.setUp(pos2)
            self.chess_engine = Board(pos_for_test_ROOK_move)
            if el not in (allowed_moves + eat_moves):
                self.assertRaises(ImpossiblePositionException, self.chess_engine.make_move, 'D4', el)
            elif el in allowed_moves:
                self.assertEqual(self.chess_engine.make_move('D4', el), [])
            elif el in eat_moves:
                self.assertEqual([self.chess_engine.make_move('D4', el)[0].get_type()], [PieceTypeEngine.PAWN])

    def test_QUEEN_move(self):
        # поставим королеву на D4
        allowed_moves = ['A4', 'B4', 'C4', 'D3', 'E4', 'F4', 'G4', 'H4', 'D5', 'D6', 'B6', 'J6', 'C5', 'I5', 'C3', 'E3',
                         'F10', 'E9']  # ,
        eat_moves = ['D7', 'A7', 'K7', 'G11']  #
        for el in cells:
            # self.setUp(pos2)
            self.chess_engine = Board(pos_for_test_QUEEN_move)
            if el not in (allowed_moves + eat_moves):
                self.assertRaises(ImpossiblePositionException, self.chess_engine.make_move, 'D4', el)
            elif el in allowed_moves:
                self.assertEqual(self.chess_engine.make_move('D4', el), [])
            elif el in eat_moves:
                self.assertEqual([self.chess_engine.make_move('D4', el)[0].get_type()], [PieceTypeEngine.PAWN])

    def test_KING_move(self):
        # поставим короля на D6
        allowed_moves = ['C6', 'I6', 'C5', 'D5', 'I5']  # ,
        eat_moves = ['C7', 'D7', 'I7']  # ,,
        for el in cells:
            # self.setUp(pos2)
            self.chess_engine = Board(pos_for_test_KING_move)
            if el not in (allowed_moves + eat_moves):
                self.assertRaises(ImpossiblePositionException, self.chess_engine.make_move, 'D6', el)
            elif el in allowed_moves:
                self.assertEqual(self.chess_engine.make_move('D6', el), [])
            elif el in eat_moves:
                self.assertEqual([self.chess_engine.make_move('D6', el)[0].get_type()], [PieceTypeEngine.PAWN])

    # проверим рокировку
    def test_castling(self):
        self.chess_engine = Board(pos_for_test_castling)
        # должны вернуться фигура ладьи и позиция, куда она перемещается
        coord = self.chess_engine.coords['F1']
        self.assertEqual(self.chess_engine.make_move('E1', 'G1'), [self.chess_engine.board[coord], 'F1'])
        self.chess_engine = Board(pos_for_test_castling)
        coord = self.chess_engine.coords['D1']
        self.assertEqual(self.chess_engine.make_move('E1', 'C1'), [self.chess_engine.board[coord], 'D1'])

    # проверим повышение пешки до ферзя
    def test_upgrade_pawn(self):
        self.chess_engine = Board(pos_test_upgrade_pawn)
        coord = self.chess_engine.coords['F1']
        # возвращает перемещаемую пешку (уже королеву), ее новый тип и цвет
        self.assertEqual(
            self.chess_engine.make_move('F2', 'F1'),
            [
                self.chess_engine.board[coord],
                self.chess_engine.board[coord].get_type(),
                PieceColorEngine.BLACK.name
            ]
        )

    # проверим возможность делать ход с пустой клетки
    def test_make_move_from_None(self):
        self.chess_engine = Board(pos_test_upgrade_pawn)
        self.assertRaises(ImpossiblePositionException, self.chess_engine.make_move, 'C5', 'C6')

    # проверим корректность возвращаемых возможных ходов
    def test_display_legal_moves_for_engine(self):
        # поставим ладью на E2
        legal_moves = ['E12', 'E11', 'E9', 'A2', 'B2', 'C2', 'D2', 'E1', 'E3', 'E4', 'F2', 'H2']
        self.chess_engine = Board(pos_check_legal_moves)
        self.assertEqual(self.chess_engine.display_legal_moves_for_engine('E2'), legal_moves)
        # при шахе
        self.chess_engine = Board(pos_check_legal_moves_for_check)
        legal_moves =['D2', 'F2']
        self.assertEqual(self.chess_engine.display_legal_moves_for_engine('E1'), legal_moves)
        self.assertEqual(self.chess_engine.display_legal_moves_for_engine('D1'), legal_moves)

    def test_check_check_and_checkmate(self):
        self.chess_engine = Board(pos_test_check)
        self.assertEqual(self.chess_engine.is_check_and_checkmate(PieceColorEngine.RED), 1)
        self.chess_engine.make_move('E1', 'E2')
        self.assertEqual(self.chess_engine.is_check_and_checkmate(PieceColorEngine.RED), 0)
        self.chess_engine = Board(pos_check_and_checkmate)
        self.assertEqual(self.chess_engine.is_check_and_checkmate(PieceColorEngine.RED), 2)
        self.chess_engine = Board(pos_check_ability_to_eat)
        self.assertEqual(self.chess_engine.is_check_and_checkmate(PieceColorEngine.RED), 1)
        self.chess_engine = Board(pos_check_ability_to_eat2)
        self.assertEqual(self.chess_engine.is_check_and_checkmate(PieceColorEngine.RED), 2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestChessEngine)
    unittest.TextTestRunner(verbosity=0).run(suite)
