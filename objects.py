
''' 
	
	contains the structure of each object

'''

import config
from config import x_fac, y_fac
import numpy as np

# bombs, walls, bricks all will be of this type
class Object:
	# the x and y coords wrt top left of board
	def __init__(self, x, y, ch = config._empty):
		self._x = x
		self._y = y
		self.width = 4
		self.height = 2
		self.is_killable = False
		self._ch = ch
		self.structure = np.chararray((self.height, self.width))
		self.structure[:, :] = self._ch
		self._type = config.types[self._ch]

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


# this is the repr of the wall object
# it implements no methods and some data about each wall element
class Wall(Object):
	# preferred size = 2 x 4
	def __init__(self, n, m):
		super(Wall, self).__init__(n, m, config._wall)
		self.height = int(m)
		self.width = int(n)

	def __repr__(self):
		for r in range(self.height):
			print("\n")
			for c in range(self.width):
				try:
					print(self.structure[r,c].decode(), end = "")
				except:
					print(self.structure[r,c], end = "")
		return ""


# this class implements the bomb object
class Bomb(Object):
	def __init__(self, x, y):
		super(Bomb, self).__init__(x, y, config._bomb)
		self.timer = 0
		self.active = False
		self.is_killable = True
		self.structure[:, :] = np.matrix([['[',self._ch,self._ch,']'],\
			['[',self._ch, self._ch, ']']])
		self.blast_radius = [(x + 1 * x_fac, y), (x + 2 * x_fac, y),\
		(x - 1 * x_fac, y), (x - 2 * x_fac, y), (x, y + 1 * y_fac), (x, y + 2 * y_fac), \
		(x, y - 1 * y_fac), (x, y - 2 * y_fac)]

	# begin detonating the bomb (happens one frame after)
	def detonate(self, time):
		self.active = True
		self.timer = time

	def countdown(self):
		if self.active:
			self.timer -= 1
			self.structure[:,1:3] = str(self.timer)
			return True
		
		if not self.timer:
			self.structure[:, :] = config._expl

	def __repr__(self):
		return "<Bomb (%d, %d) | Active : %s | %d frames left>" % \
			(self._x, self._y, self.active, self.timer)


# this class implements the bricks object 
class Bricks(Object):
	def __init__(self, x, y):
		super(Bricks, self).__init__(x, y, config._bricks)
		self.is_killable = True
		self.structure[:, :] = self._ch

	def __repr__(self):
		return "<Bomb (%d, %d) | Active : %s | %d frames left>" % \
			(self._x, self._y, self.active, self.timer)
