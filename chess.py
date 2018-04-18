from typing import Tuple
import random
import board

from PIL import Image
import itertools
import os


class Chess:
    def __init__(self):
        self.board = board.Board()
        self.gameover = False

        self.board_normal_img = Image.open('resources/board-normal.png')
        self.img_count = 0

    def save_img(self, x: int, y: int, nx: int, ny: int):
        lx = 'abcdefgh'[x]
        ly = '87654321'[y]
        lnx = 'abcdefgh'[nx]
        lny = '87654321'[ny]
        self.img_count += 1
        normal_board = f'temp/{self.img_count} - {lx}{ly} {lnx}{lny}.png'
        result_normal = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
        result_normal.paste(self.board_normal_img, (0, 0))
        chessboard = self.board.chessboard

        for y, x in itertools.product(range(8), repeat=2):
            if chessboard[y][x] is not None:
                piece_img = chessboard[y][x].pil_img
                result_normal.paste(piece_img, (x * 64, y * 64), mask=piece_img)

        if not os.path.isdir('temp/'):
            os.makedirs('temp/')

        result_normal.save(normal_board)

    def move(self, x: int, y: int, nx: int, ny: int, promote_to: str=None) -> int:
        if not self.board.gatekeeper(x, y, nx, ny, False, promote_to):
            self.save_img(x, y, nx, ny)
            # illegal move
            return 1

        else:
            # checkmate happened
            if self.board.check() and not self.board.has_legal_move():
                self.gameover = True

            # stalemate happened
            elif not self.board.has_legal_move():
                self.gameover = True

            return 0

    def ai_move(self, depth: int=3):
        # best_val, best_move = self.minimax(depth)
        legal_moves = self.board.get_legal_moves()
        if len(legal_moves) > 0:
            best_move = random.choice(legal_moves)
            x, y, nx, ny = best_move
            self.move(x, y, nx, ny, 'queen')

    def minimax(self, depth, alpha: int=-90000, beta: int=90000, is_max: bool=True):
        if depth == 0:
            return -self.board.evaluate(), None

        best_move = None
        legal_moves = self.board.get_legal_moves()
        random.shuffle(legal_moves)

        if is_max:
            best_move_val = -90000
        else:
            best_move_val = 90000

        for move in legal_moves:
            x, y, nx, ny = move
            self.move(x, y, nx, ny)
            value, _ = self.minimax(depth-1, alpha, beta, not is_max)
            self.undo()

            if is_max:
                if value > best_move_val:
                    best_move_val = value
                    best_move = move
                alpha = max(alpha, value)
            else:
                if value < best_move_val:
                    best_move_val = value
                    best_move = move
                beta = min(beta, value)

            if beta <= alpha:
                break

        return best_move_val, best_move or legal_moves[0]

    def undo(self):
        self.gameover = False
        self.board.undo()

    def status(self) -> Tuple[bool, bool]:
        # returns the current status of the game (is game over, is stalemate)
        return self.gameover, self.gameover and not self.board.check()
