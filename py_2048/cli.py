import curses
from curses import window

from . import Board

SCREEN_FMT = """{board}

Use your arrow-keys to move the tiles.
CTRL + C to quit.
"""


def run():
    curses.wrapper(loop)


def loop(stdscr: window):
    curses.curs_set(0)
    board = Board()

    while board.has_legal_moves():
        stdscr.clear()
        stdscr.addstr(SCREEN_FMT.format(board=board))

        try:
            pressed_key = stdscr.getch()
        except KeyboardInterrupt:
            break

        match pressed_key:
            case curses.KEY_LEFT:
                board.move_left()
            case curses.KEY_RIGHT:
                board.move_right()
            case curses.KEY_UP:
                board.move_up()
            case curses.KEY_DOWN:
                board.move_down()
