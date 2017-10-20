
'''

    contains the structure of each person

'''

import config
import numpy as np


class Person:

    """# bomber, enemies etc will be of this type"""

    def __init__(self, x, y, ch=config._empty):
        '''# the x and y coords wrt top left of board'''
        self._x = x
        self._y = y
        self.structure = np.chararray((2, 4))
        self.structure[:, :] = config._empty
        self._ch = ch
        self._type = config.types[self._ch]
        self.is_killable = True

    def get_type(self):
        '''# returns whether "Bomber", "Enemy", etc'''
        return self._type

    def get_size(self):
        '''# returns (height, width)'''
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

    def __repr__(self):
        return "<Person : %s | (%d, %d)>" % (self.get_type(), self._x, self._y)


class Bomber(Person):

    """# this is the class for the bomber
    # methods that the bomber can execute are written here"""

    def __init__(self, x, y, lives=config.lives[1], bombs=config.bombs[1]):
        super(Bomber, self).__init__(x, y, config._bomb_man)
        temp_skel = np.matrix([['[', self._ch, self._ch, ']'],
                               [config._empty, ']', '[', config._empty]])
        self.structure[:, :] = temp_skel
        self.lives = lives
        self.bombs = bombs
        self.score = 0
        del temp_skel


class Enemy(Person):

    """# this is the enemy class
    # enemy specific methods are added here"""

    def __init__(self, x, y):
        super(Enemy, self).__init__(x, y, config._enemy)
        temp_skel = np.matrix([['[', self._ch, self._ch, ']'],
                               [config._empty, ']', '[', config._empty]])
        self.structure[:, :] = temp_skel
        del temp_skel
