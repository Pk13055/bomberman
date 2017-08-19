'''

contains all the symbols, constants
directions, etc

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

enemies = [0, 2, 3, 4]
bricks 	= [0, 5, 7, 9]

'''
	Allow certain inputs and translate to easier to read format
	UP : 0
	DOWN : 1
	LEFT : 2
	RIGHT : 3
	BOMB : 4
'''

UP, DOWN, LEFT, RIGHT, BOMB, QUIT = range(6)

_allowed_inputs = { 
	UP 		: ['w', '\x1b[A'], \
	DOWN 	: ['s', '\x1b[B'], \
	LEFT 	: ['a', '\x1b[D'], \
	RIGHT 	: ['d', '\x1b[C'], \
	BOMB 	: ['b'],		   \
	QUIT 	: ['q']
}

def get_input(key):
	for x in _allowed_inputs:
		if key in _allowed_inputs[x]:
			return x
	return -1


# up down right left
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