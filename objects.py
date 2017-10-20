'''

    contains the structure of each object

'''

import config
from config import x_fac, y_fac
import numpy as np


class Object:

    '''# bombs, walls, bricks all will be of this type'''

    def __init__(self, x, y, ch=config._empty):
        '''# the x and y coords wrt top left of board'''
        self._x = x
        self._y = y
        self.width = 4
        self.height = 2
        self.is_killable = False
        self._ch = ch
        self.structure = np.chararray((self.height, self.width))
        self.structure[:, :] = self._ch
        self._type = config.types[self._ch]

    def get_type(self):
        '''# returns whether "Bomber", "Enemy", etc'''
        return self._type

    def get_size(self):
        '''# returns (height, willdth)'''
        return self.structure.shape

    def get_coords(self):
        '''# returns (x, y)'''
        return (self._x, self._y)

    def update_location(self, board, new_x, new_y, init=False):
        '''# update the location of the person'''
        if board.draw_obj(type(self)(new_x, new_y)):
            # if initial update, will not clear original
            if not init:
                board.clear_obj(self)
            self._x, self._y = new_x, new_y
            return True
        return False


class Wall(Object):

    '''# this is the repr of the wall object
    it implements no methods and some data about each wall element'''

    def __init__(self, n, m):
        '''# preferred size = 2 x 4'''
        super(Wall, self).__init__(n, m, config._wall)
        self.height = int(m)
        self.width = int(n)

    def __repr__(self):
        ''' repr '''
        for r in range(self.height):
            print("\n")
            for c in range(self.width):
                try:
                    print(self.structure[r, c].decode(), end="")
                except UnicodeDecodeError:
                    print(self.structure[r, c], end="")
        return ""


class Bomb(Object):

    '''# this class implements the bomb object'''

    def __init__(self, x, y):
        ''' init '''
        super(Bomb, self).__init__(x, y, config._bomb)
        self.timer = 0
        self.active = False
        self.is_killable = True
        self.structure[:, :] = np.matrix([['[', self._ch, self._ch, ']'],
                                          ['[', self._ch, self._ch, ']']])
        self.blast_radius = [(x + 1 * x_fac, y), (x + 2 * x_fac, y),
                             (x - 1 * x_fac, y), (x - 2 * x_fac, y), (x,
                                                                      y + 1 * y_fac), (x, y + 2 * y_fac),
                             (x, y - 1 * y_fac), (x, y - 2 * y_fac)]
        self.owner = None

    def detonate(self, time):
        '''# begin detonating the bomb (happens one frame after)'''
        self.active = True
        self.timer = time

    def countdown(self):
        ''' countdown the bomb when active '''
        if self.active:
            self.timer -= 1
            self.structure[:, 1:3] = str(self.timer)
            return True

        if not self.timer:
            self.structure[:, :] = config._expl

    def __repr__(self):
        ''' repr '''
        return "<Bomb (%d, %d) | Active : %s | %d frames left>" % \
            (self._x, self._y, self.active, self.timer)


class Bricks(Object):

    '''# this class implements the bricks Object'''

    def __init__(self, x, y):
        ''' init '''
        super(Bricks, self).__init__(x, y, config._bricks)
        self.is_killable = True
        self.structure[:, :] = self._ch

    def __repr__(self):
        ''' repr '''
        return "<Bomb (%d, %d) | Active : %s | %d frames left>" % \
            (self._x, self._y, self.active, self.timer)
