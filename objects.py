''' 
	Each wall element is of this type 
'''

import numpy as np
import config


# bombs, walls, bricks all will be of this type
class Object:
	def __init__(self, x, y, ch):
		self._x = x
		self._y = y
		self.width = 4
		self.height = 2
		self.dimen = (self.width, self.height)
		self.is_killable = False
		self._ch = ch
		self.structure = np.chararray(self.dimen[::-1])
		self.structure[:, :] = self._ch
		self._type = config.types[self._ch]

	def get_type(self):
		return self._type

	def get_size(self):
		return self.structure.shape

	def get_coords(self):
		return (self._x, self._y)

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

	def detonate(self, time):
		self.active = True
		self.timer = time

	def diffuse(self):
		self.active = False
		self.timer = 0

	def __repr__(self):
		return "<Bomb (%d, %d) | Active : %s | %d frames left>" % \
			(self._x, self.y, self.active, self.timer)


# this class implements the bomb object 
class Bricks(Object):
	def __init__(self, x, y):
		super(Bricks, self).__init__(x, y, config._bricks)
		self.is_killable = True
		self.structure
		pass
