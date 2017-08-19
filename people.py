
''' 
	
	contains the structure of each person

'''

import config
import numpy as np

# bomber, enemies etc will be of this type
class Person:
	# the x and y coords wrt top left of board
	def __init__(self, x, y, ch = config._empty):
		self._x = x
		self._y = y
		self.structure = np.chararray((2, 4))
		self.structure[:, :] = config._empty
		self._ch = ch
		self._type = config.types[self._ch]
		self.is_killable = True

	# returns whether "Bomber", "Enemy", etc 
	def get_type(self):
		return self._type
	
	# returns (height, width)
	def get_size(self):
		return self.structure.shape

	# returns (x, y)
	def get_coords(self):
		return (self._x, self._y)

	# update the location of the person
	def update_location(self, board, new_x, new_y, init = False):
		if board.draw_obj(type(self)(new_x, new_y)):
			# if initial update, will not clear original
			if not init:
				board.clear_obj(self)
			self._x, self._y = new_x, new_y
			return True
		return False

	def __repr__(self):
		return "<Person : %s | (%d, %d)>" % (self.get_type(), self._x, self._y)


# this is the class for the bomber 
# methods that the bomber can execute are written here 
class Bomber(Person):
	def __init__(self, x, y):
		super(Bomber, self).__init__(x, y, config._bomb_man)
		temp_skel = np.matrix([['[',self._ch,self._ch,']'],\
			[config._empty,']','[',config._empty]])
		self.structure[:, :] = temp_skel
		del temp_skel


# this is the enemy class 
# enemy specific methods are added here
class Enemy(Person):
	def __init__(self, x, y):
		super(Enemy, self).__init__(x, y, config._enemy)
		temp_skel = np.matrix([['[',self._ch, self._ch,']'],\
			[config._empty,']','[',config._empty]])
		self.structure[:, :] = temp_skel
		del temp_skel
		
