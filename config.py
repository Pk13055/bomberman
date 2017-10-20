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
# scores
scores = {
    _bricks : 20,
    _enemy : 100
}
# number of properties per level (0 is debug)
enemies = [0, 2, 3, 4]
bricks = [0, 5, 7, 9]
lives = [10, 3, 5, 7]
bombs = [20, 5, 6, 7]
timelimit = [100, 90, 90, 80]
timers = [
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
    UP      : ['w', '\x1b[A'], \
    DOWN    : ['s', '\x1b[B'], \
    LEFT    : ['a', '\x1b[D'], \
    RIGHT   : ['d', '\x1b[C'], \
    BOMB    : ['b'],           \
    QUIT    : ['q']
}

def get_key(key):
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


    def __call__(self):
        return self.impl()


class _GetchUnix:


    def __init__(self):
        import tty, sys


    def __call__(self):
        import sys
        import tty
        import termios
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


_getch = _Getch()


class AlarmException(Exception):
    pass


def alarmHandler(signum, frame):
    raise AlarmException


def get_input(timeout=1):
    import signal
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.alarm(timeout)
    try:
        text = _getch()
        signal.alarm(0)
        return text
    except AlarmException:
        pass
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''

# for printing colored people
colors = {
    'Black'            : '\x1b[0;30m',
    'Blue'             : '\x1b[0;34m',
    'Green'            : '\x1b[0;32m',
    'Cyan'             : '\x1b[0;36m',
    'Red'              : '\x1b[0;31m',
    'Purple'           : '\x1b[0;35m',
    'Brown'            : '\x1b[0;33m',
    'Gray'             : '\x1b[0;37m',
    'Dark Gray'        : '\x1b[1;30m',
    'Light Blue'       : '\x1b[1;34m',
    'Light Green'      : '\x1b[1;32m',
    'Light Cyan'       : '\x1b[1;36m',
    'Light Red'        : '\x1b[1;31m',
    'Light Purple'     : '\x1b[1;35m',
    'Yellow'           : '\x1b[1;33m',
    'White'            : '\x1b[1;37m'
}

ENDC = '\x1b[0m'


def getcc(ch):

    try:
        if ch == _empty:
            return ch
        elif ch == _wall:
            color = 'Dark Gray'
        elif ch == _bomb_man:
            color = 'Blue'
        elif ch == _enemy:
            color = 'Red'
        elif ch == _bricks:
            color = 'Brown'
        elif ch == _expl:
            color = 'Yellow'
        elif ch in [str(x) for x in range(10)]:
            color = 'White'
        elif ch == '[' or ch == ']':
            color = 'Purple'
        else:
            color = 'None'
        return colors[color] + ch + ENDC
    except KeyError:
        return ch


def printcc(st, color):
    try:
        return colors[color] + st + ENDC
    except KeyError:
        return st
