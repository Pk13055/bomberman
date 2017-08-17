
''' 
	
	contains the structure of each person

'''

import config
import numpy as np

class Person:
	# the x and y coords denote the 
	def __init__(self, x, y, ch = config._empty):
		self.x = x
		self.y = y
		self.structure = np.chararray((2, 4))
		self.structure[:, :] = config._empty
		self._ch = ch
		self._type = config.types[self._ch]

	def get_size(self):
		return self.structure.shape

	def get_type(self):
		return self._type

	def update_location(self, board, new_x, new_y):
		s_height, s_width = self.get_size()

	# update the frame for every action taken
	def update_frame(b):
		try:
			b.frame_counter += 1
			return True
		except: 
			return False

	def __repr__(self):
		return "<Person : %s | (%d, %d)>" % (self.get_type(), self.x, self.y)


# this is the class for the bomber 
# methods that the bomber can execute are 
class Bomber(Person):
	def __init__(self, x, y):
		super(Bomber, self).__init__(x, y, config._bomb_man)
		temp_skel = np.matrix([['[','^','^',']'],\
			[config._empty,']','[',config._empty]])
		self.structure[:, :] = temp_skel
		del temp_skel
 
class Enemy(Person):
	def __init__(self, x, y):
		super(Enemy, self).__init__(x, y, config._enemy)
		temp_skel = np.matrix([['[',config._enemy, config._enemy,']'],\
			[config._empty,']','[',config._empty]])
		self.structure[:, :] = temp_skel
		del temp_skel
		
