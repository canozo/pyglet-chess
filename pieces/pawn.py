from .piece import Piece
from typing import List
import pyglet


class Pawn(Piece):
    def __init__(self, is_white: bool, has_moved: bool=False, pinned: bool=False):
        super(Pawn, self).__init__(is_white, has_moved, pinned)
        if self.is_white:
            self.img = pyglet.sprite.Sprite(pyglet.image.load('resources/pawn-w.png'))
        else:
            self.img = pyglet.sprite.Sprite(pyglet.image.load('resources/pawn-b.png'))

    def __deepcopy__(self, memodict):
        return Pawn(self.is_white, self.has_moved, self.pinned)

    def check_laser(self, chessboard, x, y, check_mode):
        return []

    def can_move(self, x: int, y: int, new_x: int, new_y: int, piece_in_path: bool) -> bool:
        dx = abs(x-new_x)
        dy = y-new_y

        if self.is_white:
            dy = -dy

        if dx == 0 and dy == 1 and not piece_in_path:
            return True
        elif dx == 1 and dy == 1 and piece_in_path:
            return True
        elif dx == 0 and dy == 2 and not piece_in_path and not self.has_moved:
            return True

        return False

    def controlled(self, table: List[List[bool]], chessboard: List[List[Piece]], x: int, y: int) -> List[List[bool]]:
        if (self.is_white and y == 7) or (not self.is_white and y == 0):
            return table

        if self.is_white:
            dy = y+1
        else:
            dy = y-1

        if x < 7:
            table[dy][x+1] = True
        if x > 0:
            table[dy][x-1] = True

        return table
