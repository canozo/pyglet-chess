from typing import Tuple
import random
import board


class Chess:
    def __init__(self):
        self.board = board.Board()
        self.gameover = False

    def move(self, x: int, y: int, nx: int, ny: int, promote_to: str=None) -> int:
        if not self.board.gatekeeper(x, y, nx, ny, False, promote_to):
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

    def ai_move(self):
        legal_moves = self.board.get_legal_moves()
        if len(legal_moves) > 0:
            # value = -9000
            # best_move = (0, 0, 0, 0)
            # for move in legal_moves:
            #     move_val = self.board.evaluate(move)
            #     if move_val > value:
            #         best_move = move
            #         value = move_val

            best_move = random.choice(legal_moves)

            x, y, nx, ny = best_move
            self.move(x, y, nx, ny, 'queen')

    def status(self) -> Tuple[bool, bool]:
        # returns the current status of the game (is game over, is stalemate)
        return self.gameover, self.gameover and not self.board.check()
