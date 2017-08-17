'''

contains all the symbols to be used

'''

_wall = "X"
_bricks = "/"
_bomb_man = "B"
_enemy = "E"
_expl = "e"
_bomb = "O"
_empty = " "

types = {
	
	_empty : "Unassigned",
	
	_wall : "Wall",
	_bomb : "Bomb",
	_bricks : "Bricks",
	
	_bomb_man : "Bomber",
	_enemy : "Enemy"
}

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()