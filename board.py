''' 
	Contains the board class along with the methods and other features
'''

from objects import Wall
import numpy as np
import config

def printb(b):
	for r in range(b.shape[0]):
		for c in range(b.shape[-1]):
			try:
				print(b[r,c].decode(), end = "")
			except:
				print(b[r,c], end = "")
		print()

# preferred size = 42 x 84
class Board:
	def __init__(self, m, n):
		
		assert(type(n) == int)
		assert(type(m) == int)

		self.width = n
		self.height = m
		self.dimen = (n, m)
		self._b = np.chararray((m, n))
		self._b[:, :] = config._empty
		self.frame_counter = 0
		self.init_board()
		
		# this stores all the bombs bricks and enemies that spawn
		self._storage = {
			config.types[config._bomb] : [],
			config.types[config._bricks] : [],
			config.types[config._enemy] : []
		}

	def clear_storage(self):
		for object_type in self._storage:
			for  object_ in self._storage[object_type]:
				del object_
			self._storage[object_type] = []

	# reset the borad at the end of a life 
	def reset_board(self):
		reset = True
		self.init_board(reset)
		self.clear_storage()
	
	# initialize and setup the frame of the board
	def init_board(self, reset = False):
		if reset:
			self.frame_counter = 0
		# scaling the wall piece
		w = Wall(self.width / 20, self.height / 20)
		w_width, w_height = w.dimen
		
		# creating the rows
		full_row, full_row[:, :] = \
			np.chararray((w_height, self.width)), config._wall
		emp_row, emp_row[:, :] = \
			np.chararray((w_height, self.width)), config._empty
		emp_row[:, :w_width] = emp_row[:, -w_width:] = w.structure

		alt_row, alt_row[:, :] = \
			np.chararray((w_height, self.width)), config._empty
		for c in range(1, int(self.width / w_width) + 1):
			if c % 2:
				alt_row[:, (c - 1) * w_width: (c * w_width)] = w.structure

		# assigning top and bottom
		self._b[:w_height, :] = self._b[-w_height:, :] = full_row
		# assigning other rows
		for r in range(2, int(self.height / w_height)):
			# alt row
			if r % 2:
				cur_row = alt_row
			else:
				cur_row = emp_row

			self._b[(r - 1) * w_height: (r * w_height), : ] = cur_row
	
	# check if anything else if occupied
	def path_clear(self, obj):
		return True

	# size being a (height, width) tuple
	def attach_object(self, obj):
		if self.path_clear(obj):
			# add code to bind object to the board as well
			try:
				self._storage[obj.get_type()].append(obj)
				height, width = obj.get_size()
				x, y = obj.x - 1, obj.y - 1
				self._b[y: y + height, x: x + width ] = obj.structure
				return True
			except KeyError:
				print("Cannot attach the given object")
				return False
		else:
			return False

	# method to spawn the main player
	def spawn(self, obj):
		if obj.get_type() == config.types[config._bomb_man]:
			return True
		else:
			print("Cannot spawn non-player object")
			return False

	# displaying the board at every frame
	def render(self):
		pass

	# printing the board for debugging purposes
	def __repr__(self):
		temp_board = np.matrix(self._b)
		for row in range(self.height):
			for col in range(self.width):
				try:
					print(temp_board[row, col].decode(), end = "") 
				except:
					print(temp_board[row, col], end = "") 
			print()
		del temp_board
		return ""
