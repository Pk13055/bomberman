'''

contains all the symbols, constants
directions, etc

'''

# ch repr of objects
_wall = "X"
_bricks = "/"
_bomb_man = "B"
_enemy = "E"
_expl = "e"
_bomb = "O"
_empty = " "

# types of objects
types = {
	
	_empty : "Unassigned",
	
	_wall : "Wall",
	_bomb : "Bomb",
	_bricks : "Bricks",
	
	_bomb_man : "Bomber",
	_enemy : "Enemy"
}

# number of properties per level (0 is debug)
enemies = [0, 2, 3, 4]
bricks 	= [0, 5, 7, 9]
lives   = [10, 3, 5, 7]
bombs   = [20, 5, 6, 7]
timers  = [
    [5],
    [5],
    [5, 7],
    [4, 6, 9]
]

# scaling and move factor
x_fac, y_fac = (4, 2)


'''
	Allow certain inputs and translate to easier to read format
	UP : 0
	DOWN : 1
	LEFT : 2
	RIGHT : 3
	BOMB : 4
'''

# key presses
UP, DOWN, LEFT, RIGHT, BOMB, QUIT = range(6)
DIR = [UP, DOWN, LEFT, RIGHT]
INVALID = -1

# allowed inputs
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
	return INVALID


# Gets a single character from standard input.  Does not echo to the screen.
class _Getch:
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