from .piece import Piece
from typing import List, Tuple
import pyglet
from PIL import Image


class Rook(Piece):
    def __init__(self, is_white: bool, has_moved: bool=False):
        super(Rook, self).__init__(is_white, has_moved)
        if self.is_white:
            self.img = pyglet.sprite.Sprite(pyglet.image.load('resources/rook-w.png'))
            self.pil_img = Image.open('resources/rook-w.png')
        else:
            self.img = pyglet.sprite.Sprite(pyglet.image.load('resources/rook-b.png'))
            self.pil_img = Image.open('resources/rook-b.png')

    def __deepcopy__(self, memodict):
        return Rook(self.is_white, self.has_moved)

    def check_laser(self, chessboard: List[List[Piece]], x: int, y: int,
                    check_mode: bool=False) -> List[Tuple[int, int]]:
        return self.get_laser((-1, 0, 1, 0, -1), chessboard, x, y, check_mode)

    def can_move(self, x: int, y: int, new_x: int, new_y: int, piece_in_path: bool) -> bool:
        dx = abs(x-new_x)
        dy = abs(y-new_y)
        return (dx == 0 and dy != 0) or (dx != 0 and dy == 0)

    def controlled(self, table: List[List[bool]], chessboard: List[List[Piece]], x: int, y: int) -> List[List[bool]]:
        return self.possible_moves((-1, 0, 1, 0, -1), table, chessboard, x, y)
