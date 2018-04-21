from .piece import Piece
from typing import List, Tuple


class Rook(Piece):
    @staticmethod
    def check_laser(chessboard: List[List[str]], x: int, y: int,
                    is_white: bool, check_mode: bool=False) -> List[Tuple[int, int]]:
        return Piece.get_laser((-1, 0, 1, 0, -1), chessboard, x, y, is_white, check_mode)

    @staticmethod
    def can_move(x: int, y: int, new_x: int, new_y: int, piece_in_path: bool, is_white: bool) -> bool:
        dx = abs(x-new_x)
        dy = abs(y-new_y)
        return (dx == 0 and dy != 0) or (dx != 0 and dy == 0)

    @staticmethod
    def controlled(table: List[List[bool]], chessboard: List[List[str]],
                   x: int, y: int, is_white: bool) -> List[List[bool]]:
        return Piece.possible_moves((-1, 0, 1, 0, -1), table, chessboard, x, y)
