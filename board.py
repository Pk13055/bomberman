''' 
	Contains the board class along with the methods and other features
'''

from objects import Wall
import numpy as np
import config
import sys
from os import system

 # preferred size = (34, 76)
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
		self.init_points = []
		
		self.init_board()

		# this stores all the bombs bricks and enemies that spawn
		self._storage = {
			config.types[config._bomb] : [],
			config.types[config._bricks] : [],
			config.types[config._enemy] : []
		}

	
	# initialize and setup the frame of the board
	def init_board(self, reset = False):
		if reset:
			self.frame_counter = 0
		# scaling the wall piece
		w = Wall(self.width / 20, self.height / 20)
		w_height, w_width  = w.get_size()
		
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

		# create the inital points for spawning objects
		# subtracting two edge blocks for each top bottom and dividing by two for range of motion
		fp, x_fac, y_fac = (5, 3), 4, 2
		total_block_x = int((self.width / x_fac - 2) / 2 + 1)  # each object is 4 px wide
		total_block_y = int((self.height / y_fac  - 2) / 2 + 1) # each object is 2px tall
		for r in range(total_block_x):
			for c in range(total_block_y):
				self.init_points.append( (fp[0] + r * (2 * x_fac), fp[-1] + c * (2 * y_fac)) )
		self.init_points = list(set(self.init_points))

	# reset the borad at the end of a life 
	def reset_board(self):
		reset = True
		self.init_board(reset)
		self.clear_storage()


	# main function to check updates at every frame
	def update_frame(self):
		self.frame_counter += 1

	# check if new binding space is occupied else if occupied
	def path_clear(self, obj):
		height, width =  obj.get_size()
		x_pos, y_pos = obj.get_coords()
		
		emp_comp = np.chararray(obj.get_size())
		emp_comp[:, :] = config._empty

		return np.all(self._b[y_pos - 1: y_pos - 1 + height, x_pos - 1:\
		 x_pos - 1 + width] == emp_comp)


	# add to storage
	def add_storage(self, obj):
		try:
			if obj not in self._storage[obj.get_type()]:
				self._storage[obj.get_type()].append(obj)
				return True
			else:
				return None
		except KeyError:
			return False

	# clear the objects on the board at every instance
	def clear_storage(self, obj = None):
		if obj is None:
			for object_type in self._storage:
				for  object_ in self._storage[object_type]:
					del object_
				self._storage[object_type] = []
			return True
		else:
			typ = obj.get_type()
			try:
				ind =  self._storage[typ].index(obj)
				self._storage[typ] = self._storage[typ][:ind] \
					+ self._storage[typ][ind + 1:]
				return True
			except:
				return False

	# draws the object on the board
	def draw_obj(self, obj):
		if self.path_clear(obj):
			height, width = obj.get_size()
			x, y = obj.get_coords()
			self._b[y - 1: y - 1 + height, x - 1: x - 1 + width] = obj.structure
			return True
		return False	

	# clears the object from the board by an object
	def clear_obj(self, obj):
		if obj.get_type() != config.types[config._wall]:
			height, width = obj.get_size()
			x, y = obj.get_coords()
			self._b[y - 1: y - 1 + height, x - 1: x - 1 + width] = config._empty
			return True
		return False

	# size being a (height, width) tuple
	def attach_object(self, obj):
		if self.draw_obj(obj):
			self.add_storage(obj)
			return True
		return False

	# method to spawn the main player
	def spawn(self, obj):
		if obj.get_type() == config.types[config._bomb_man]:
			height, width = obj.get_size()
			x, y = obj.get_coords()
			x, y = x - 1, y - 1
			self._b[y: y + height, x: x + width ] = obj.structure
			return True
		else:
			print("Cannot spawn non-player object")
			return False

	# to process the key press and take according action
	def process_input(self, key_press):
		return True
		if key_press == config.UP:
			pass
		elif key_press == config.DOWN:
			pass
		elif key_press == config.LEFT:
			pass
		elif key_press == config.RIGHT:
			pass
		elif key_press == config.BOMB:		
			pass



	# displaying the board at every frame
	def render(self):
		sys.stdout.flush()
		# print("\x1b[{};{}H".format(0,0))
		try:
			system('clear')
		except:
			system('cls')

		temp_board = np.matrix(self._b)
		for row in range(self.height):
			for col in range(self.width):
				try:
					sys.stdout.write(temp_board[row, col].decode()) 
				except:
					sys.stdout.write(temp_board[row, col]) 
			sys.stdout.write("\n")
		del temp_board

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
