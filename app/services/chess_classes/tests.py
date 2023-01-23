import unittest

from app.services.chess_classes.board import Board
from app.services.chess_classes.color import PieceColor
from app.services.chess_classes.impossible_position_exception import ImpossiblePositionException
from app.services.chess_classes.piece_type import PieceType

pos_base = [[PieceType.QUEEN, PieceColor.WHITE, 'I8'], [PieceType.KING, PieceColor.WHITE, 'D8'],
            [PieceType.ROOK, PieceColor.WHITE, 'A8'], [PieceType.ROOK, PieceColor.WHITE, 'L8'],
            [PieceType.BISHOP, PieceColor.WHITE, 'J8'], [PieceType.BISHOP, PieceColor.WHITE, 'C8'],
            [PieceType.KNIGHT, PieceColor.WHITE, 'B8'], [PieceType.KNIGHT, PieceColor.WHITE, 'K8'],
            [PieceType.PAWN, PieceColor.WHITE, 'A7'], [PieceType.PAWN, PieceColor.WHITE, 'B7'],
            [PieceType.PAWN, PieceColor.WHITE, 'C7'], [PieceType.PAWN, PieceColor.WHITE, 'D7'],
            [PieceType.PAWN, PieceColor.WHITE, 'I7'], [PieceType.PAWN, PieceColor.WHITE, 'J7'],
            [PieceType.PAWN, PieceColor.WHITE, 'K7'], [PieceType.PAWN, PieceColor.WHITE, 'L7'],
            [PieceType.QUEEN, PieceColor.BLACK, 'E12'], [PieceType.KING, PieceColor.BLACK, 'I12'],
            [PieceType.ROOK, PieceColor.BLACK, 'H12'], [PieceType.ROOK, PieceColor.BLACK, 'L12'],
            [PieceType.BISHOP, PieceColor.BLACK, 'F12'], [PieceType.BISHOP, PieceColor.BLACK, 'J12'],
            [PieceType.KNIGHT, PieceColor.BLACK, 'G12'], [PieceType.KNIGHT, PieceColor.BLACK, 'K12'],
            [PieceType.PAWN, PieceColor.BLACK, 'L11'], [PieceType.PAWN, PieceColor.BLACK, 'K11'],
            [PieceType.PAWN, PieceColor.BLACK, 'J11'], [PieceType.PAWN, PieceColor.BLACK, 'I11'],
            [PieceType.PAWN, PieceColor.BLACK, 'E11'], [PieceType.PAWN, PieceColor.BLACK, 'F11'],
            [PieceType.PAWN, PieceColor.BLACK, 'G11'], [PieceType.PAWN, PieceColor.BLACK, 'H11'],

            [PieceType.QUEEN, PieceColor.RED, 'D1'], [PieceType.KING, PieceColor.RED, 'E1'],
            [PieceType.ROOK, PieceColor.RED, 'A1'], [PieceType.ROOK, PieceColor.RED, 'H1'],
            [PieceType.BISHOP, PieceColor.RED, 'C1'], [PieceType.BISHOP, PieceColor.RED, 'F1'],
            [PieceType.KNIGHT, PieceColor.RED, 'B1'], [PieceType.KNIGHT, PieceColor.RED, 'G1'],
            [PieceType.PAWN, PieceColor.RED, 'A2'], [PieceType.PAWN, PieceColor.RED, 'B2'],
            [PieceType.PAWN, PieceColor.RED, 'C2'], [PieceType.PAWN, PieceColor.RED, 'D2'],
            [PieceType.PAWN, PieceColor.RED, 'E2'], [PieceType.PAWN, PieceColor.RED, 'F2'],
            [PieceType.PAWN, PieceColor.RED, 'G2'], [PieceType.PAWN, PieceColor.RED, 'H2']
            ]
pos_for_test_PAWN_move = [[PieceType.QUEEN, PieceColor.WHITE, 'I8'], [PieceType.KING, PieceColor.WHITE, 'D8'],
                          [PieceType.ROOK, PieceColor.WHITE, 'A8'], [PieceType.ROOK, PieceColor.WHITE, 'L8'],
                          [PieceType.BISHOP, PieceColor.WHITE, 'J8'], [PieceType.BISHOP, PieceColor.WHITE, 'C8'],
                          [PieceType.KNIGHT, PieceColor.WHITE, 'B8'], [PieceType.KNIGHT, PieceColor.WHITE, 'K8'],
                          [PieceType.PAWN, PieceColor.WHITE, 'A7'], [PieceType.PAWN, PieceColor.WHITE, 'B7'],
                          [PieceType.PAWN, PieceColor.WHITE, 'C7'], [PieceType.PAWN, PieceColor.WHITE, 'D3'],
                          [PieceType.PAWN, PieceColor.WHITE, 'I7'], [PieceType.PAWN, PieceColor.WHITE, 'J7'],
                          [PieceType.PAWN, PieceColor.WHITE, 'K7'], [PieceType.PAWN, PieceColor.WHITE, 'L7'],

                          [PieceType.QUEEN, PieceColor.BLACK, 'E12'], [PieceType.KING, PieceColor.BLACK, 'I12'],
                          [PieceType.ROOK, PieceColor.BLACK, 'H12'], [PieceType.ROOK, PieceColor.BLACK, 'L12'],
                          [PieceType.BISHOP, PieceColor.BLACK, 'F12'], [PieceType.BISHOP, PieceColor.BLACK, 'J12'],
                          [PieceType.KNIGHT, PieceColor.BLACK, 'G12'], [PieceType.KNIGHT, PieceColor.BLACK, 'K12'],
                          [PieceType.PAWN, PieceColor.BLACK, 'L11'], [PieceType.PAWN, PieceColor.BLACK, 'K11'],
                          [PieceType.PAWN, PieceColor.BLACK, 'J11'], [PieceType.PAWN, PieceColor.BLACK, 'I9'],
                          [PieceType.PAWN, PieceColor.BLACK, 'E9'], [PieceType.PAWN, PieceColor.BLACK, 'F11'],
                          [PieceType.PAWN, PieceColor.BLACK, 'G11'], [PieceType.PAWN, PieceColor.BLACK, 'H11'],

                          [PieceType.QUEEN, PieceColor.RED, 'D1'], [PieceType.KING, PieceColor.RED, 'E1'],
                          [PieceType.ROOK, PieceColor.RED, 'A1'], [PieceType.ROOK, PieceColor.RED, 'H1'],
                          [PieceType.BISHOP, PieceColor.RED, 'C1'], [PieceType.BISHOP, PieceColor.RED, 'F1'],
                          [PieceType.KNIGHT, PieceColor.RED, 'B1'], [PieceType.KNIGHT, PieceColor.RED, 'G1'],
                          [PieceType.PAWN, PieceColor.RED, 'A2'], [PieceType.PAWN, PieceColor.RED, 'B2'],
                          [PieceType.PAWN, PieceColor.RED, 'C2'], [PieceType.PAWN, PieceColor.RED, 'D2'],
                          [PieceType.PAWN, PieceColor.RED, 'E4'], [PieceType.PAWN, PieceColor.RED, 'F2'],
                          [PieceType.PAWN, PieceColor.RED, 'G2'], [PieceType.PAWN, PieceColor.RED, 'H2']
                          ]
pos_for_test_KNIGHT_move = [[PieceType.QUEEN, PieceColor.WHITE, 'I8'], [PieceType.KING, PieceColor.WHITE, 'D8'],
                            [PieceType.ROOK, PieceColor.WHITE, 'A8'], [PieceType.ROOK, PieceColor.WHITE, 'L8'],
                            [PieceType.BISHOP, PieceColor.WHITE, 'J8'], [PieceType.BISHOP, PieceColor.WHITE, 'C8'],
                            [PieceType.KNIGHT, PieceColor.WHITE, 'B8'], [PieceType.KNIGHT, PieceColor.WHITE, 'K8'],
                            [PieceType.PAWN, PieceColor.WHITE, 'A7'], [PieceType.PAWN, PieceColor.WHITE, 'B7'],
                            [PieceType.PAWN, PieceColor.WHITE, 'C7'], [PieceType.PAWN, PieceColor.WHITE, 'D7'],
                            [PieceType.PAWN, PieceColor.WHITE, 'I7'], [PieceType.PAWN, PieceColor.WHITE, 'J7'],
                            [PieceType.PAWN, PieceColor.WHITE, 'K7'], [PieceType.PAWN, PieceColor.WHITE, 'L7'],
                            [PieceType.QUEEN, PieceColor.BLACK, 'E12'], [PieceType.KING, PieceColor.BLACK, 'I12'],
                            [PieceType.ROOK, PieceColor.BLACK, 'H12'], [PieceType.ROOK, PieceColor.BLACK, 'L12'],
                            [PieceType.BISHOP, PieceColor.BLACK, 'F12'], [PieceType.BISHOP, PieceColor.BLACK, 'J12'],
                            [PieceType.KNIGHT, PieceColor.BLACK, 'G12'], [PieceType.KNIGHT, PieceColor.BLACK, 'K12'],
                            [PieceType.PAWN, PieceColor.BLACK, 'L11'], [PieceType.PAWN, PieceColor.BLACK, 'K11'],
                            [PieceType.PAWN, PieceColor.BLACK, 'J11'], [PieceType.PAWN, PieceColor.BLACK, 'I11'],
                            [PieceType.PAWN, PieceColor.BLACK, 'E11'], [PieceType.PAWN, PieceColor.BLACK, 'F11'],
                            [PieceType.PAWN, PieceColor.BLACK, 'G11'], [PieceType.PAWN, PieceColor.BLACK, 'H11'],

                            [PieceType.QUEEN, PieceColor.RED, 'D1'], [PieceType.KING, PieceColor.RED, 'E1'],
                            [PieceType.ROOK, PieceColor.RED, 'A1'], [PieceType.ROOK, PieceColor.RED, 'H1'],
                            [PieceType.BISHOP, PieceColor.RED, 'C1'], [PieceType.BISHOP, PieceColor.RED, 'F1'],
                            [PieceType.KNIGHT, PieceColor.RED, 'B1'], [PieceType.KNIGHT, PieceColor.RED, 'G9'],
                            [PieceType.PAWN, PieceColor.RED, 'A2'], [PieceType.PAWN, PieceColor.RED, 'B2'],
                            [PieceType.PAWN, PieceColor.RED, 'C2'], [PieceType.PAWN, PieceColor.RED, 'D2'],
                            [PieceType.PAWN, PieceColor.RED, 'E2'], [PieceType.PAWN, PieceColor.RED, 'F2'],
                            [PieceType.PAWN, PieceColor.RED, 'G2'], [PieceType.PAWN, PieceColor.RED, 'H2']
                            ]
pos_for_test_BISHOP_move = [[PieceType.QUEEN, PieceColor.WHITE, 'I8'], [PieceType.KING, PieceColor.WHITE, 'D8'],
                            [PieceType.ROOK, PieceColor.WHITE, 'A8'], [PieceType.ROOK, PieceColor.WHITE, 'L8'],
                            [PieceType.BISHOP, PieceColor.WHITE, 'J8'], [PieceType.BISHOP, PieceColor.WHITE, 'C8'],
                            [PieceType.KNIGHT, PieceColor.WHITE, 'B8'], [PieceType.KNIGHT, PieceColor.WHITE, 'K8'],
                            [PieceType.PAWN, PieceColor.WHITE, 'A7'], [PieceType.PAWN, PieceColor.WHITE, 'B7'],
                            [PieceType.PAWN, PieceColor.WHITE, 'C7'], [PieceType.PAWN, PieceColor.WHITE, 'D7'],
                            [PieceType.PAWN, PieceColor.WHITE, 'I7'], [PieceType.PAWN, PieceColor.WHITE, 'J7'],
                            [PieceType.PAWN, PieceColor.WHITE, 'K7'], [PieceType.PAWN, PieceColor.WHITE, 'L7'],
                            [PieceType.QUEEN, PieceColor.BLACK, 'E12'], [PieceType.KING, PieceColor.BLACK, 'I12'],
                            [PieceType.ROOK, PieceColor.BLACK, 'H12'], [PieceType.ROOK, PieceColor.BLACK, 'L12'],
                            [PieceType.BISHOP, PieceColor.BLACK, 'F12'], [PieceType.BISHOP, PieceColor.BLACK, 'J12'],
                            [PieceType.KNIGHT, PieceColor.BLACK, 'G12'], [PieceType.KNIGHT, PieceColor.BLACK, 'K12'],
                            [PieceType.PAWN, PieceColor.BLACK, 'L11'], [PieceType.PAWN, PieceColor.BLACK, 'K11'],
                            [PieceType.PAWN, PieceColor.BLACK, 'J11'], [PieceType.PAWN, PieceColor.BLACK, 'I11'],
                            [PieceType.PAWN, PieceColor.BLACK, 'E11'], [PieceType.PAWN, PieceColor.BLACK, 'F11'],
                            [PieceType.PAWN, PieceColor.BLACK, 'G11'], [PieceType.PAWN, PieceColor.BLACK, 'H11'],

                            [PieceType.QUEEN, PieceColor.RED, 'D1'], [PieceType.KING, PieceColor.RED, 'E1'],
                            [PieceType.ROOK, PieceColor.RED, 'A1'], [PieceType.ROOK, PieceColor.RED, 'H1'],
                            [PieceType.BISHOP, PieceColor.RED, 'C5'], [PieceType.BISHOP, PieceColor.RED, 'F1'],
                            [PieceType.KNIGHT, PieceColor.RED, 'B1'], [PieceType.KNIGHT, PieceColor.RED, 'G1'],
                            [PieceType.PAWN, PieceColor.RED, 'A2'], [PieceType.PAWN, PieceColor.RED, 'B2'],
                            [PieceType.PAWN, PieceColor.RED, 'C2'], [PieceType.PAWN, PieceColor.RED, 'D2'],
                            [PieceType.PAWN, PieceColor.RED, 'E2'], [PieceType.PAWN, PieceColor.RED, 'F2'],
                            [PieceType.PAWN, PieceColor.RED, 'G2'], [PieceType.PAWN, PieceColor.RED, 'H2']
                            ]
pos_for_test_ROOK_move = [[PieceType.QUEEN, PieceColor.WHITE, 'I8'], [PieceType.KING, PieceColor.WHITE, 'D8'],
                          [PieceType.ROOK, PieceColor.WHITE, 'A8'], [PieceType.ROOK, PieceColor.WHITE, 'L8'],
                          [PieceType.BISHOP, PieceColor.WHITE, 'J8'], [PieceType.BISHOP, PieceColor.WHITE, 'C8'],
                          [PieceType.KNIGHT, PieceColor.WHITE, 'B8'], [PieceType.KNIGHT, PieceColor.WHITE, 'K8'],
                          [PieceType.PAWN, PieceColor.WHITE, 'A7'], [PieceType.PAWN, PieceColor.WHITE, 'B7'],
                          [PieceType.PAWN, PieceColor.WHITE, 'C7'], [PieceType.PAWN, PieceColor.WHITE, 'D7'],
                          [PieceType.PAWN, PieceColor.WHITE, 'I7'], [PieceType.PAWN, PieceColor.WHITE, 'J7'],
                          [PieceType.PAWN, PieceColor.WHITE, 'K7'], [PieceType.PAWN, PieceColor.WHITE, 'L7'],
                          [PieceType.QUEEN, PieceColor.BLACK, 'E12'], [PieceType.KING, PieceColor.BLACK, 'I12'],
                          [PieceType.ROOK, PieceColor.BLACK, 'H12'], [PieceType.ROOK, PieceColor.BLACK, 'L12'],
                          [PieceType.BISHOP, PieceColor.BLACK, 'F12'], [PieceType.BISHOP, PieceColor.BLACK, 'J12'],
                          [PieceType.KNIGHT, PieceColor.BLACK, 'G12'], [PieceType.KNIGHT, PieceColor.BLACK, 'K12'],
                          [PieceType.PAWN, PieceColor.BLACK, 'L11'], [PieceType.PAWN, PieceColor.BLACK, 'K11'],
                          [PieceType.PAWN, PieceColor.BLACK, 'J11'], [PieceType.PAWN, PieceColor.BLACK, 'I11'],
                          [PieceType.PAWN, PieceColor.BLACK, 'E11'], [PieceType.PAWN, PieceColor.BLACK, 'F11'],
                          [PieceType.PAWN, PieceColor.BLACK, 'G11'], [PieceType.PAWN, PieceColor.BLACK, 'H11'],

                          [PieceType.QUEEN, PieceColor.RED, 'D1'], [PieceType.KING, PieceColor.RED, 'E1'],
                          [PieceType.ROOK, PieceColor.RED, 'D4'], [PieceType.ROOK, PieceColor.RED, 'H1'],
                          [PieceType.BISHOP, PieceColor.RED, 'C1'], [PieceType.BISHOP, PieceColor.RED, 'F1'],
                          [PieceType.KNIGHT, PieceColor.RED, 'B1'], [PieceType.KNIGHT, PieceColor.RED, 'G1'],
                          [PieceType.PAWN, PieceColor.RED, 'A2'], [PieceType.PAWN, PieceColor.RED, 'B2'],
                          [PieceType.PAWN, PieceColor.RED, 'C2'], [PieceType.PAWN, PieceColor.RED, 'D2'],
                          [PieceType.PAWN, PieceColor.RED, 'E2'], [PieceType.PAWN, PieceColor.RED, 'F2'],
                          [PieceType.PAWN, PieceColor.RED, 'G2'], [PieceType.PAWN, PieceColor.RED, 'H2']
                          ]
pos_for_test_QUEEN_move = [[PieceType.QUEEN, PieceColor.WHITE, 'I8'], [PieceType.KING, PieceColor.WHITE, 'D8'],
                           [PieceType.ROOK, PieceColor.WHITE, 'A8'], [PieceType.ROOK, PieceColor.WHITE, 'L8'],
                           [PieceType.BISHOP, PieceColor.WHITE, 'J8'], [PieceType.BISHOP, PieceColor.WHITE, 'C8'],
                           [PieceType.KNIGHT, PieceColor.WHITE, 'B8'], [PieceType.KNIGHT, PieceColor.WHITE, 'K8'],
                           [PieceType.PAWN, PieceColor.WHITE, 'A7'], [PieceType.PAWN, PieceColor.WHITE, 'B7'],
                           [PieceType.PAWN, PieceColor.WHITE, 'C7'], [PieceType.PAWN, PieceColor.WHITE, 'D7'],
                           [PieceType.PAWN, PieceColor.WHITE, 'I7'], [PieceType.PAWN, PieceColor.WHITE, 'J7'],
                           [PieceType.PAWN, PieceColor.WHITE, 'K7'], [PieceType.PAWN, PieceColor.WHITE, 'L7'],
                           [PieceType.QUEEN, PieceColor.BLACK, 'E12'], [PieceType.KING, PieceColor.BLACK, 'I12'],
                           [PieceType.ROOK, PieceColor.BLACK, 'H12'], [PieceType.ROOK, PieceColor.BLACK, 'L12'],
                           [PieceType.BISHOP, PieceColor.BLACK, 'F12'], [PieceType.BISHOP, PieceColor.BLACK, 'J12'],
                           [PieceType.KNIGHT, PieceColor.BLACK, 'G12'], [PieceType.KNIGHT, PieceColor.BLACK, 'K12'],
                           [PieceType.PAWN, PieceColor.BLACK, 'L11'], [PieceType.PAWN, PieceColor.BLACK, 'K11'],
                           [PieceType.PAWN, PieceColor.BLACK, 'J11'], [PieceType.PAWN, PieceColor.BLACK, 'I11'],
                           [PieceType.PAWN, PieceColor.BLACK, 'E11'], [PieceType.PAWN, PieceColor.BLACK, 'F11'],
                           [PieceType.PAWN, PieceColor.BLACK, 'G11'], [PieceType.PAWN, PieceColor.BLACK, 'H11'],

                           [PieceType.QUEEN, PieceColor.RED, 'D4'], [PieceType.KING, PieceColor.RED, 'E1'],
                           [PieceType.ROOK, PieceColor.RED, 'A1'], [PieceType.ROOK, PieceColor.RED, 'H1'],
                           [PieceType.BISHOP, PieceColor.RED, 'C1'], [PieceType.BISHOP, PieceColor.RED, 'F1'],
                           [PieceType.KNIGHT, PieceColor.RED, 'B1'], [PieceType.KNIGHT, PieceColor.RED, 'G1'],
                           [PieceType.PAWN, PieceColor.RED, 'A2'], [PieceType.PAWN, PieceColor.RED, 'B2'],
                           [PieceType.PAWN, PieceColor.RED, 'C2'], [PieceType.PAWN, PieceColor.RED, 'D2'],
                           [PieceType.PAWN, PieceColor.RED, 'E2'], [PieceType.PAWN, PieceColor.RED, 'F2'],
                           [PieceType.PAWN, PieceColor.RED, 'G2'], [PieceType.PAWN, PieceColor.RED, 'H2']
                           ]
pos_for_test_KING_move = [[PieceType.QUEEN, PieceColor.WHITE, 'I8'], [PieceType.KING, PieceColor.WHITE, 'D6'],
                          [PieceType.ROOK, PieceColor.WHITE, 'A8'], [PieceType.ROOK, PieceColor.WHITE, 'L8'],
                          [PieceType.BISHOP, PieceColor.WHITE, 'J8'], [PieceType.BISHOP, PieceColor.WHITE, 'C8'],
                          [PieceType.KNIGHT, PieceColor.WHITE, 'B8'], [PieceType.KNIGHT, PieceColor.WHITE, 'K8'],
                          [PieceType.PAWN, PieceColor.WHITE, 'A7'], [PieceType.PAWN, PieceColor.WHITE, 'B7'],
                          [PieceType.PAWN, PieceColor.WHITE, 'C7'], [PieceType.PAWN, PieceColor.WHITE, 'D7'],
                          [PieceType.PAWN, PieceColor.WHITE, 'I7'], [PieceType.PAWN, PieceColor.WHITE, 'J7'],
                          [PieceType.PAWN, PieceColor.WHITE, 'K7'], [PieceType.PAWN, PieceColor.WHITE, 'L7'],
                          [PieceType.QUEEN, PieceColor.BLACK, 'E12'], [PieceType.KING, PieceColor.BLACK, 'I12'],
                          [PieceType.ROOK, PieceColor.BLACK, 'H12'], [PieceType.ROOK, PieceColor.BLACK, 'L12'],
                          [PieceType.BISHOP, PieceColor.BLACK, 'F12'], [PieceType.BISHOP, PieceColor.BLACK, 'J12'],
                          [PieceType.KNIGHT, PieceColor.BLACK, 'G12'], [PieceType.KNIGHT, PieceColor.BLACK, 'K12'],
                          [PieceType.PAWN, PieceColor.BLACK, 'L11'], [PieceType.PAWN, PieceColor.BLACK, 'K11'],
                          [PieceType.PAWN, PieceColor.BLACK, 'J11'], [PieceType.PAWN, PieceColor.BLACK, 'I11'],
                          [PieceType.PAWN, PieceColor.BLACK, 'E11'], [PieceType.PAWN, PieceColor.BLACK, 'F11'],
                          [PieceType.PAWN, PieceColor.BLACK, 'G11'], [PieceType.PAWN, PieceColor.BLACK, 'H11'],

                          [PieceType.QUEEN, PieceColor.RED, 'D1'], [PieceType.KING, PieceColor.RED, 'D6'],
                          [PieceType.ROOK, PieceColor.RED, 'A1'], [PieceType.ROOK, PieceColor.RED, 'H1'],
                          [PieceType.BISHOP, PieceColor.RED, 'C1'], [PieceType.BISHOP, PieceColor.RED, 'F1'],
                          [PieceType.KNIGHT, PieceColor.RED, 'B1'], [PieceType.KNIGHT, PieceColor.RED, 'G1'],
                          [PieceType.PAWN, PieceColor.RED, 'A2'], [PieceType.PAWN, PieceColor.RED, 'B2'],
                          [PieceType.PAWN, PieceColor.RED, 'C2'], [PieceType.PAWN, PieceColor.RED, 'D2'],
                          [PieceType.PAWN, PieceColor.RED, 'E2'], [PieceType.PAWN, PieceColor.RED, 'F2'],
                          [PieceType.PAWN, PieceColor.RED, 'G2'], [PieceType.PAWN, PieceColor.RED, 'H2']
                          ]
pos_for_test_castling = [
    [PieceType.KING, PieceColor.RED, 'E1'],
    [PieceType.ROOK, PieceColor.RED, 'A1'], [PieceType.ROOK, PieceColor.RED, 'H1'],
]
pos_test_upgrade_pawn = [[PieceType.PAWN, PieceColor.BLACK, 'F2']]
pos_test_check = [[PieceType.KING, PieceColor.RED, 'E1'], [PieceType.BISHOP, PieceColor.WHITE, 'G3']]
pos_check_and_checkmate = [[PieceType.KING, PieceColor.RED, 'E1'], [PieceType.BISHOP, PieceColor.WHITE, 'H3'],
                           [PieceType.QUEEN, PieceColor.WHITE, 'C2'], [PieceType.ROOK, PieceColor.WHITE, 'E4']]
pos_check_ability_to_eat = [[PieceType.KING, PieceColor.RED, 'E1'], [PieceType.BISHOP, PieceColor.WHITE, 'H3'],
                            [PieceType.QUEEN, PieceColor.WHITE, 'D2'], [PieceType.ROOK, PieceColor.WHITE, 'E4']]
# дамку прикрывает ладья
pos_check_ability_to_eat2 = [[PieceType.KING, PieceColor.RED, 'E1'], [PieceType.BISHOP, PieceColor.WHITE, 'H3'],
                             [PieceType.QUEEN, PieceColor.WHITE, 'D2'], [PieceType.ROOK, PieceColor.BLACK, 'D3']]

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
                self.assertEqual([self.chess_engine.make_move('E4', el)[0].get_type()], [PieceType.PAWN])

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
                self.assertEqual([self.chess_engine.make_move('G9', el)[0].get_type()], [PieceType.PAWN])

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
                self.assertEqual([self.chess_engine.make_move('C5', el)[0].get_type()], [PieceType.PAWN])

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
                self.assertEqual([self.chess_engine.make_move('D4', el)[0].get_type()], [PieceType.PAWN])

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
                self.assertEqual([self.chess_engine.make_move('D4', el)[0].get_type()], [PieceType.PAWN])

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
                self.assertEqual([self.chess_engine.make_move('D6', el)[0].get_type()], [PieceType.PAWN])

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
                PieceColor.BLACK.name
            ]
        )

    # проверим возможность делать ход с пустой клетки
    def test_make_move_from_None(self):
        self.chess_engine = Board(pos_test_upgrade_pawn)
        self.assertRaises(ImpossiblePositionException, self.chess_engine.make_move, 'C5', 'C6')

    # проверим корректность возвращаемых возможных ходов
    def test_display_legal_moves_for_engine(self):
        # поставим ладью на D4
        legal_moves = ['D7', 'D6', 'D5', 'A4', 'B4', 'C4', 'D3', 'E4', 'F4', 'G4', 'H4']
        self.chess_engine = Board(pos_for_test_ROOK_move)
        self.assertEqual(self.chess_engine.display_legal_moves_for_engine('D4'), legal_moves)

    def test_check_check_and_checkmate(self):
        self.chess_engine = Board(pos_test_check)
        self.assertEqual(self.chess_engine.is_check_and_checkmate(PieceColor.RED), 1)
        self.chess_engine.make_move('E1', 'E2')
        self.assertEqual(self.chess_engine.is_check_and_checkmate(PieceColor.RED), 0)
        self.chess_engine = Board(pos_check_and_checkmate)
        self.assertEqual(self.chess_engine.is_check_and_checkmate(PieceColor.RED), 2)
        self.chess_engine = Board(pos_check_ability_to_eat)
        self.assertEqual(self.chess_engine.is_check_and_checkmate(PieceColor.RED), 1)
        self.chess_engine = Board(pos_check_ability_to_eat2)
        self.assertEqual(self.chess_engine.is_check_and_checkmate(PieceColor.RED), 2)
