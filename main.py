from chess import Chess
from pyglet.window import mouse
from pyglet.window import key
import pyglet
import itertools


game_window = pyglet.window.Window(height=512, width=512)
message_label = pyglet.text.Label(font_name='Times New Roman',
                                  font_size=36,
                                  color=(35, 203, 35, 255),
                                  x=game_window.width // 2,
                                  y=game_window.height // 2,
                                  anchor_x='center',
                                  anchor_y='center')
board_normal = pyglet.sprite.Sprite(pyglet.image.load('resources/board-normal.png'))
piece_held = None
match = Chess()
ai_mode = False
promotion = None
old_pos = (0, 0)


@game_window.event
def on_draw():
    game_window.clear()
    board_normal.draw()
    chessboard = match.board.chessboard

    for x, y in itertools.product(range(8), repeat=2):
        if chessboard[y][x] is not None:
            piece = chessboard[y][x]
            if piece is not piece_held:
                piece.img.x = x * 64
                piece.img.y = 448 - y * 64
            piece.img.draw()

    gameover, stalemate = match.status()
    if stalemate:
        message_label.text = 'Stalemate!'
        message_label.draw()
    elif gameover:
        if match.board.white_turn:
            message_label.text = 'Checkmate. Black won!'
        else:
            message_label.text = 'Checkmate. White won!'
        message_label.draw()


@game_window.event
def on_mouse_press(x, y, button, modifiers):
    global piece_held, old_pos
    if button == mouse.LEFT and not match.gameover:
        chessboard = match.board.chessboard
        piece = chessboard[7 - y//64][x//64]
        if piece is not None:
            piece_held = piece
            old_pos = (x//64, 7 - y//64)


@game_window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if piece_held is not None:
        piece_held.img.x = x - 32
        piece_held.img.y = y - 32


@game_window.event
def on_mouse_release(x, y, button, modifiers):
    global piece_held
    if piece_held is not None:
        dx, dy = x//64, 7 - y//64
        ox, oy = old_pos
        error = match.move(ox, oy, dx, dy, promotion)
        if not error and ai_mode:
            match.ai_move()

    piece_held = None


@game_window.event
def on_key_press(symbol, modifiers):
    global match, promotion, ai_mode
    if symbol == key.N:
        match = Chess()
    elif symbol == key.A:
        ai_mode = not ai_mode
    elif symbol == key.U:
        match.board.undo()
    elif symbol == key.Q:
        promotion = 'queen'
    elif symbol == key.B:
        promotion = 'bishop'
    elif symbol == key.R:
        promotion = 'rook'
    elif symbol == key.K:
        promotion = 'knight'


@game_window.event
def on_key_release(symbol, modifiers):
    global promotion
    if symbol in (key.Q, key.B, key.R, key.K):
        promotion = None


def main():
    pyglet.app.run()


if __name__ == '__main__':
    main()
